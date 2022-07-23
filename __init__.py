from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from services.log import logger
from utils.manager import withdraw_message_manager
from configs.config import Config
import requests

__zx_plugin_name__ = "video"
__plugin_usage__ = """
usage：
    看视频吗哥哥？
    指令：
        视频/sp/来点视频/video
""".strip()
__plugin_des__ = "看视频吗？"
__plugin_cmd__ = ["视频|sp"]
__plugin_version__ = 0.1
__plugin_author__ = 'Shouzi'
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["视频", "sp", "来点视频", "video"],
}
__plugin_configs__ = {
    "WITHDRAW_VIDEO_MESSAGE": {
        "value": (60, 1),
        "help": "自动撤回，参1：延迟撤回色图时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
        "default_value": (0, 1),
    },
}


video = on_regex("^(sp|视频|来点视频|video)$", priority=5, block=True)

url = "https://v.api.aa1.cn/api/api-dy-girl/index.php?aa1=ajdu987hrjfw"


@video.handle()
async def send_video(bot: Bot, event: Event, state: T_State):
    mp4 = requests.get(url)
    video_msg = r"[CQ:video,file="+mp4.url+"]"
    try:
        msg_id = await video.send(Message(video_msg))
        withdraw_message_manager.withdraw_message(
            event,
            msg_id["message_id"],
            Config.get_config("video", "WITHDRAW_VIDEO_MESSAGE"),
        )
    except Exception as e:
        logger.error(f"xjjvideo 发送了未知错误 {type(e)}：{e}")
