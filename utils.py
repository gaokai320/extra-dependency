import pandas as pd
from packaging.markers import UndefinedEnvironmentName
from packaging.requirements import InvalidRequirement, Requirement
from pymongo import MongoClient
from tqdm import tqdm

tqdm.pandas()

db = MongoClient(host="127.0.0.1", port=27017)["pypi"]


def check_single_spec_extras(requirement_str: str):
    try:
        req = Requirement(requirement_str)
    except InvalidRequirement:
        return False
    except:
        return False
    marker = req.marker
    if marker is not None:
        try:
            marker.evaluate()
        except UndefinedEnvironmentName:
            return True
        except:
            return False
    return False


def requires_dist_specify_extras(x):
    for dep_spec in x:
        if check_single_spec_extras(dep_spec):
            return True
    return False


def merge_same_distribution(x):
    home_page = x[pd.notna(x["home_page"])]["home_page"]
    if home_page.empty:
        home_page = ""
    else:
        home_page = home_page.iloc[0]

    project_urls = x[pd.notna(x["project_urls"])]["project_urls"]
    if project_urls.empty:
        project_urls = ""
    else:
        project_urls = project_urls.iloc[0]

    if not x[x["extra"]].empty:
        tmp = x[x["extra"]].iloc[0]
        requires_dist = tmp["requires_dist"]
        upload_time = tmp["upload_time"]
        size = tmp["size"]
        extra = tmp["extra"]
    else:
        tmp = x[x["requires_dist"].str.len() != 0]
        if tmp.empty:
            tmp = x.iloc[0]
        else:
            tmp = tmp.iloc[0]
        requires_dist = tmp["requires_dist"]
        upload_time = tmp["upload_time"]
        size = tmp["size"]
        extra = tmp["extra"]
    return pd.Series(
        {
            "requires_dist": requires_dist,
            "extra": extra,
            "upload_time": upload_time,
            "size": size,
            "home_page": home_page,
            "project_urls": project_urls,
        }
    )


def simplify_metadata():
    """
    Keep only `name`, `version`, `requires_dist`, etc.
    """
    dm_col = db["distribution_metadata"]
    df = pd.DataFrame(
        dm_col.find(
            {},
            projection={
                "_id": 0,
                "name": 1,
                "version": 1,
                "upload_time": 1,
                "project_urls": 1,
                "home_page": 1,
                "requires_dist": 1,
                "size": 1,
            },
        )
    )
    # check whether a distribution' requires_dist specify extras\
    # About 1 hour 20 minutes to run
    df["extra"] = df["requires_dist"].progress_apply(requires_dist_specify_extras)
    # merge information of distributions with the same `name` and `version`
    # About a 1 hour 20 minutes to run
    df = (
        df.groupby(["name", "version"])
        .progress_apply(merge_same_distribution)
        .reset_index()
    )

    db["packages"].drop()
    package_col = db["packages"]
    package_col.insert_many(df.to_dict("records"))


def package_by_year():
    pass


if __name__ == "__main__":
    simplify_metadata()