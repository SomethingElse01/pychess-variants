from misc import time_control_str

MAX_USER_SEEKS = 10


class Seek:
    gen_id = 0

    def __init__(self, user, variant, fen="", color="r", base=5, inc=3, byoyomi_period=0, level=6, rated=False, chess960=False, alternate_start="", target="", ws=None):
        self.user = user
        self.variant = variant
        self.color = color
        self.fen = "" if fen is None else fen
        self.rated = rated
        self.rating = int(round(user.get_rating(variant, chess960).mu, 0))
        self.base = base
        self.inc = inc
        self.byoyomi_period = byoyomi_period
        self.level = 0 if user.username == "Random-Mover" else level
        self.chess960 = chess960
        self.alternate_start = alternate_start
        self.target = target
        self.ws = ws

        Seek.gen_id += 1
        self.id = self.gen_id

        self.as_json = {
            "seekID": self.id,
            "user": self.user.username,
            "bot": self.user.bot,
            "title": self.user.title,
            "variant": self.variant,
            "chess960": self.chess960,
            "alternateStart": self.alternate_start,
            "target": self.target,
            "fen": self.fen,
            "color": self.color,
            "rated": self.rated,
            "rating": self.rating,
            "tc": time_control_str(self.base, self.inc, self.byoyomi_period)
        }


def create_seek(seeks, user, data, ws=None):
    if len(user.seeks) >= MAX_USER_SEEKS:
        return None

    seek = Seek(
        user, data["variant"],
        fen=data["fen"],
        color=data["color"],
        base=data["minutes"],
        inc=data["increment"],
        byoyomi_period=data["byoyomiPeriod"],
        rated=data.get("rated"),
        chess960=data.get("chess960"),
        alternate_start=data.get("alternateStart"),
        target=data.get("target"),
        ws=ws)

    seeks[seek.id] = seek
    user.seeks[seek.id] = seek


def get_seeks(seeks):
    return {"type": "get_seeks", "seeks": [seek.as_json for seek in seeks.values()]}


def challenge(seek, gameId):
    return '{"type":"challenge", "challenge": {"id":"%s", "challenger":{"name":"%s", "rating":1500,"title":""},"variant":{"key":"%s"},"rated":"true","timeControl":{"type":"clock","limit":300,"increment":0},"color":"random","speed":"rapid","perf":{"name":"Rapid"}, "level":%s, "chess960":%s}}\n' % (gameId, seek.user.username, seek.variant, seek.level, str(seek.chess960).lower())
