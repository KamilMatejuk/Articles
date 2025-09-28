import pandas as pd


#################################### read ######################################

def split_df_by_month(df: pd.DataFrame):
    df['date'] = pd.to_datetime(df['date'])
    return [group for _, group in df.groupby([df['date'].dt.year, df['date'].dt.month])]

def _remove_honeymoon(df: pd.DataFrame):
    start = pd.to_datetime("2025-08-20")
    end = pd.to_datetime("2025-09-14")
    return df[~df["date"].between(start, end)]

################################## calculate ##################################

def get_monthly_points_and_labels(df: pd.DataFrame):
    linkedin_post = _calc_linkedin_post(df)
    df = _remove_honeymoon(df)
    return {
        'sleep': _calc_sleep(df), # health - avg
        'nap': _calc_nap(df), # health - passrate

        'side projects': _calc_projects(df), # time - passrate
        'read': _calc_read(df), # time - passrate
        'phone': _calc_phone(df), # time - avg

        'exercise': _calc_exercise(df), # health - passrate
        'shoulder raises': _calc_shoulder_raises(df), # health - passrate
        'pushups': _calc_pushups(df), # health - passrate
        'abs': _calc_abs(df), # health - passrate
        
        'alcohol': _calc_alcohol(df), # diet - passrate
        'kcal': _calc_kcal(df), # diet - passrate
        'creatine': _calc_creatine(df), # diet - passrate
        'tongkatali': _calc_tongkatali(df), # diet - passrate
        
        'linkedin_post': linkedin_post, # social - number
        'linkedin comment': _calc_linkedin_comment(df), # social - number
        'medium': _calc_medium(df), # social - number
    }

def _to_time(n: float):
    h = int(n / 60)
    m = int(n % 60)
    return (f'{h}h ' if h else '') + f'{m}m'

def _calc_sleep(df: pd.DataFrame):
    # average sleep (min 7h) per night
    value = df['sleep'].mean()
    return value, _to_time(value)

def _calc_nap(df: pd.DataFrame):
    # no naps during the day
    value = df['nap'].sum()
    return 1 - (value / len(df)), f'missed {value} days'

def _calc_projects(df: pd.DataFrame):
    # side projects every day
    value = sum(df['side_projects_time'] >= 15) / len(df)
    return value, f'{value:.1%}'

def _calc_read(df: pd.DataFrame):
    # reading every day
    value = sum(df['read_time'] >= 5) / len(df)
    return value, f'{value:.1%}'

def _calc_phone(df: pd.DataFrame):
    # average phone usage (max 3h) per day
    value = df['phone_time'].mean()
    return value, _to_time(value)

def _calc_exercise(df: pd.DataFrame):
    # exercise every day
    value = sum(df['exercise_time'] >= 5) / len(df)
    return value, f'{value:.1%}'

def _calc_shoulder_raises(df: pd.DataFrame):
    # shoulder raises every day
    df = df[df["date"] >= pd.to_datetime("2024-11-04")]
    if len(df) == 0: return None, ''
    value = df['shoulder_raises'].sum() / len(df)
    return value, f'{value:.1%}'

def _calc_pushups(df: pd.DataFrame):
    # pushups every day
    df = df[df["date"] >= pd.to_datetime("2025-06-19")]
    if len(df) == 0: return None, ''
    value = df['pushups'].sum() / len(df)
    return value, f'{value:.1%}'

def _calc_abs(df: pd.DataFrame):
    # abs every day
    df = df[df["date"] >= pd.to_datetime("2025-06-19")]
    if len(df) == 0: return None, ''
    value = df['abs'].sum() / len(df)
    return value, f'{value:.1%}'

def _calc_alcohol(df: pd.DataFrame):
    # no alcohol
    value = df['alcohol'].sum()
    return 1 - (value / len(df)), f'missed {value} days'

def _calc_kcal(df: pd.DataFrame):
    month = df.reset_index().at[0, 'date'].month
    if month in [10, 11, 12, 1, 2, 3, 4]:
        # between 2500 and 3000
        value = sum((df['kcal'] >= 2500) & (df['kcal'] <= 3000)) / len(df)
        return value, f'{value:.1%}'
    if month in [5, 6, 7, 8, 9]:
        # between 2000 and 2500
        value = sum((df['kcal'] >= 2000) & (df['kcal'] <= 2500)) / len(df)
        return value, f'{value:.1%}'

def _calc_creatine(df: pd.DataFrame):
    # creatine every day
    df = df[df["date"] >= pd.to_datetime("2025-04-01")]
    if len(df) == 0: return None, ''
    value = df['creatine'].sum() / len(df)
    return value, f'{value:.1%}'

def _calc_tongkatali(df: pd.DataFrame):
    # tongatali every day
    start = pd.to_datetime("2025-05-13")
    end = pd.to_datetime("2025-07-09")
    df = df[df["date"].between(start, end)]
    if len(df) == 0: return None, ''
    value = df['tongkat ali'].sum() / len(df)
    return value, f'{value:.1%}'

def _calc_linkedin_post(df: pd.DataFrame):
    # number of posts
    df = df[df["date"] >= pd.to_datetime("2024-12-02")]
    if len(df) == 0: return None, ''
    value = df['linkedin_post'].sum()
    return value, f'{value} posts' if value != 1 else '1 post'

def _calc_linkedin_comment(df: pd.DataFrame):
    # number of comments
    df = df[df["date"] >= pd.to_datetime("2025-06-18")]
    if len(df) == 0: return None, ''
    value = df['linkedin_comment'].sum()
    return value, f'{value} comments' if value != 1 else '1 comment'

def _calc_medium(df: pd.DataFrame):
    # number of articles
    value = df['medium'].sum()
    return value, f'{value} articles' if value != 1 else '1 article'

#################################### draw #####################################

def draw_spider_chart(df: pd.DataFrame, month: int):
    ...

if __name__ == "__main__":
    df = pd.read_csv("data.csv")
    dfs = split_df_by_month(df)
    data = [get_monthly_points_and_labels(month_df) for month_df in dfs]
    for d in data: print(d)