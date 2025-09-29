import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation

################################### parser ####################################

class Parser:
    @staticmethod
    def _to_time(n: float):
        h = int(n / 60)
        m = int(n % 60)
        return (f'{h}h ' if h else '') + f'{m}m'

    @staticmethod
    def _scale(v: float, minimum: float, maximum: float):
        value = (v - minimum) / (maximum - minimum)
        return max(min(value, 1), 0)

    @staticmethod
    def split_df_by_month(df: pd.DataFrame):
        df['date'] = pd.to_datetime(df['date'])
        groups = [group for _, group in df.groupby([df['date'].dt.year, df['date'].dt.month])]
        return [(g, g.reset_index().at[0, 'date'].month) for g in groups]

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def _remove_honeymoon(self):
        start = pd.to_datetime("2025-08-20")
        end = pd.to_datetime("2025-09-14")
        self.df = self.df[~self.df["date"].between(start, end)]

    def get_monthly_points_and_labels(self):
        linkedin_post = self._calc_linkedin_post()
        self._remove_honeymoon()
        results = {
            'Side\nProjects': self._calc_projects(), # time - passrate
            'Reading': self._calc_read(), # time - passrate
            'Phone': self._calc_phone(), # time - avg
            'No Naps': self._calc_nap(), # health - passrate
            'Sleep': self._calc_sleep(), # health - avg
            'Exercise': self._calc_exercise(), # health - passrate
            'Shoulder\nraises': self._calc_shoulder_raises(), # health - passrate
            'Pushups': self._calc_pushups(), # health - passrate
            'Abs': self._calc_abs(), # health - passrate
            'No Alcohol': self._calc_alcohol(), # diet - passrate
            'Calories': self._calc_kcal(), # diet - passrate
            'Creatine': self._calc_creatine(), # diet - passrate
            'Tongkat Ali': self._calc_tongkatali(), # diet - passrate
            'Medium\nArticle': self._calc_medium(), # social - number
            'LinkedIn\nPost': linkedin_post, # social - number
            'LinkedIn\nComment': self._calc_linkedin_comment(), # social - number
        }
        categories = [k if v is not None else '' for k, (v, _) in results.items()]
        points = [v for v, _ in results.values()]
        annotations = [l for _, l in results.values()]
        return categories, points, annotations

    def _calc_sleep(self):
        # average sleep (min 7h) per night
        value = self.df['sleep'].mean()
        # scale 6h - 7.5h
        return self._scale(value, 6 * 60, 7.5 * 60), self._to_time(value)

    def _calc_nap(self):
        # no naps during the day
        value = self.df['nap'].sum()
        return 1 - (value / len(self.df)), f'missed\n{value} days'

    def _calc_projects(self):
        # side projects every day
        value = sum(self.df['side_projects_time'] >= 15) / len(self.df)
        return value, f'{value:.1%}'

    def _calc_read(self):
        # reading every day
        value = sum(self.df['read_time'] >= 5) / len(self.df)
        return value, f'{value:.1%}'

    def _calc_phone(self):
        # average phone usage (max 3h) per day
        value = self.df['phone_time'].mean()
        # scale 3h - 2h
        return self._scale(value, 3 * 60, 2 * 60), self._to_time(value)

    def _calc_exercise(self):
        # exercise every day
        value = sum(self.df['exercise_time'] >= 5) / len(self.df)
        return value, f'{value:.1%}'

    def _calc_shoulder_raises(self):
        # shoulder raises every day
        df = self.df[self.df["date"] >= pd.to_datetime("2024-11-04")]
        if len(df) == 0: return None, ''
        value = df['shoulder_raises'].sum() / len(df)
        return value, f'{value:.1%}'

    def _calc_pushups(self):
        # pushups every day
        df = self.df[self.df["date"] >= pd.to_datetime("2025-06-19")]
        if len(df) == 0: return None, ''
        value = df['pushups'].sum() / len(df)
        return value, f'{value:.1%}'

    def _calc_abs(self):
        # abs every day
        df = self.df[self.df["date"] >= pd.to_datetime("2025-06-19")]
        if len(df) == 0: return None, ''
        value = df['abs'].sum() / len(df)
        return value, f'{value:.1%}'

    def _calc_alcohol(self):
        # no alcohol
        value = self.df['alcohol'].sum()
        return 1 - (value / len(self.df)), f'missed\n{value} days'

    def _calc_kcal(self):
        month = self.df.reset_index().at[0, 'date'].month
        if month in [10, 11, 12, 1, 2, 3, 4]:
            # between 2500 and 3000
            value = sum((self.df['kcal'] >= 2500) & (self.df['kcal'] <= 3000)) / len(self.df)
            return value, f'{value:.1%}'
        if month in [5, 6, 7, 8, 9]:
            # between 2000 and 2500
            value = sum((self.df['kcal'] >= 2000) & (self.df['kcal'] <= 2500)) / len(self.df)
            return value, f'{value:.1%}'

    def _calc_creatine(self):
        # creatine every day
        df = self.df[self.df["date"] >= pd.to_datetime("2025-04-01")]
        if len(df) == 0: return None, ''
        value = df['creatine'].sum() / len(df)
        return value, f'{value:.1%}'

    def _calc_tongkatali(self):
        # tongatali every day
        start = pd.to_datetime("2025-05-13")
        end = pd.to_datetime("2025-07-09")
        df = self.df[self.df["date"].between(start, end)]
        if len(df) == 0: return None, ''
        value = df['tongkat ali'].sum() / len(df)
        return value, f'{value:.1%}'

    def _calc_linkedin_post(self):
        # number of posts
        df = self.df[self.df["date"] >= pd.to_datetime("2024-12-02")]
        if len(df) == 0: return None, ''
        value = df['linkedin_post'].sum()
        # scale 0 - 15
        return self._scale(value, 0, 15), f'{value} posts' if value != 1 else '1 post'

    def _calc_linkedin_comment(self):
        # number of comments
        df = self.df[self.df["date"] >= pd.to_datetime("2025-06-18")]
        if len(df) == 0: return None, ''
        value = df['linkedin_comment'].sum()
        # scale 0 - 20
        return self._scale(value, 0, 20), f'{value} comments' if value != 1 else '1 comment'

    def _calc_medium(self):
        # number of articles
        value = self.df['medium'].sum()
        # scale 0 - 2
        return self._scale(value, 0, 2), f'{value} articles' if value != 1 else '1 article'

################################## animator ###################################

class Animator(FuncAnimation):
    def __init__(self, data: list[tuple[str, list, list, list]], filename: str, seconds_per_month: float, seconds_per_transition: float, fps: int):
        self.data = data
        self.scores = {month: np.mean([p for p in points if p is not None]) for month, _, points, _ in data}
        self.months = {month: self._month_name(month) for month, _, _, _ in data}
        self.colors = [plt.cm.winter(i) for i in np.linspace(0, 1, 13)]
        self.angles = np.linspace(0, 2 * np.pi, max(len(categories) for _, categories, _, _ in data), endpoint=False).tolist()
        self.angles += self.angles[:1]
        self.fig = plt.figure(figsize=(10, 10))
        gs = gridspec.GridSpec(15, 1, figure=self.fig)
        self.ax1 = self.fig.add_subplot(gs[:14, 0], polar=True)  # top 90%
        self.ax2 = self.fig.add_subplot(gs[14:, 0])              # bottom 10%
        self.frames_per_month = int(seconds_per_month * fps)
        self.frames_per_transition = int(seconds_per_transition * fps)
        # forth all months and back without first and last month
        frames_forth = list(range(len(data) * self.frames_per_month + (len(data) - 1) * self.frames_per_transition))
        frames_back = frames_forth[-self.frames_per_month-1:self.frames_per_month:-1]
        frames_back_and_forth = frames_forth + frames_back
        self.progress = tqdm.tqdm(total=len(frames_back_and_forth) + 1, desc="Processing")
        super().__init__(self.fig, self.update, frames=frames_back_and_forth, interval=1000 / fps, repeat=True)
        super().save(filename, fps=fps)
        self.progress.close()
    
    def _month_name(self, month: int):
        year = 2025 if month <= 9 else 2024
        month = pd.to_datetime(f'2025-{month:02}-01').month_name()
        return f'{month} {year}'
        
    def update(self, frame):
        self.progress.update(1)
        empty_value = 0.1
        month_index = frame // (self.frames_per_month + self.frames_per_transition)
        transition = ((frame % (self.frames_per_month + self.frames_per_transition)) - self.frames_per_month) / self.frames_per_transition
        if transition < 0:
            month, categories, points, annotations = self.data[month_index]
            points = [p if p is not None else empty_value for p in points]
            return self.draw_spider_chart(month, categories, points, annotations, month_index)
        prev_month, prev_categories, prev_points, prev_annotations = self.data[month_index]
        next_month, next_categories, next_points, next_annotations = self.data[month_index + 1]
        prev_points = [p if p is not None else empty_value for p in prev_points]
        next_points = [p if p is not None else empty_value for p in next_points]
        self.draw_spider_chart(
            prev_month if transition < 0.5 else next_month,
            prev_categories if transition < 0.5 else next_categories,
            [(1 - transition) * p1 + transition * p2 for p1, p2 in zip(prev_points, next_points)],
            prev_annotations if transition < 0.5 else next_annotations,
            month_index if transition < 0.5 else month_index + 1,
            transition
        )

    def draw_spider_chart(self, month: str, categories: list[str], points: list[float], annotations: list[str], index: int, transition: float = None):
        self.ax1.clear()
        self.ax1.fill(self.angles, points + points[:1], color=self.colors[index], alpha=0.25)
        self.ax1.plot(self.angles, points + points[:1], color=self.colors[index], linewidth=2)
        scatter_angles = [a for a, c in zip(self.angles, categories) if c != '']
        scatter_points = [p for p, c in zip(points, categories) if c != '']
        self.ax1.scatter(scatter_angles + scatter_angles[:1], scatter_points + scatter_points[:1], color=self.colors[index], marker='o', s=50, zorder=5)
        self.ax1.set_ylim(-0.1, 1.1)
        self.ax1.set_yticklabels([])
        self.ax1.set_xticks(self.angles[:-1])
        self.ax1.set_xticklabels([])
        self.ax1.set_title(self.months[month], size=20, y=1.1)
        for category, annotation, value, angle in zip(categories, annotations, points, self.angles):
            ha = 'right' if np.pi * 0.5 < angle < np.pi * 1.5 else 'left'
            self.ax1.text(angle, 1.2, category, ha=ha, va='center', fontsize=12)
            if value is None: continue
            text_kwargs = dict(ha='center', va='center', fontsize=12, color="#AA5E00")
            self.ax1.text(angle, value + 0.1, annotation, **text_kwargs)
        self.ax1.text(0, -0.1, f"{self.scores[month]:.0%}", ha='center', va='center', fontsize=14, fontweight="bold")
        self.ax2.clear()
        self.ax2.set_yticks([])
        self.ax2.set_xticks(range(13))
        self.ax2.set_xticklabels([''] + [self._month_name(m) for m in list(range(10, 13)) + list(range(1, 10))], rotation=45, ha='right')
        self.ax2.set_xlim(0.75, 12)
        pbar = index + 1 if transition is None else (index + transition + 1 if transition < 0.5 else index + transition)
        self.ax2.barh(0, pbar, color=self.colors[index], alpha=0.25)
        self.fig.tight_layout()


if __name__ == "__main__":
    df = pd.read_csv("data.csv")
    dfs = Parser.split_df_by_month(df)
    data = [(month, *Parser(month_df).get_monthly_points_and_labels()) for month_df, month in dfs]
    Animator(data, "spider_chart.gif", seconds_per_month=1.5, seconds_per_transition=0.5, fps=12)

