from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from services.log import logger
from utils.manager import withdraw_message_manager
from configs.config import Config
import requests
from typing import Tuple, Any
from nonebot.params import RegexGroup


from nonebot.plugin import PluginMetadata

from zhenxun.configs.config import Config
from zhenxun.configs.path_config import TEMP_PATH
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.withdraw_manage import WithdrawManager

__zx_plugin_name__ = "video"
__plugin_usage__ = """
usage：
    看视频吗哥哥？
    指令：
        视频/sp/来点视频/video
    示例：
        5连sp
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


__plugin_meta__ = PluginMetadata(
    name="随机视频",
    description="可以随机视频 的 Nonebot 插件",
    usage="""
    视频/sp/来点视频/video
    示例: 视频/sp/来点视频/video
    """.strip(),
    extra=PluginExtraData(
        author="shouzi",
        version="0.1",
        configs=[
            RegisterConfig(
                key="WITHDRAW_VIDEO_MESSAGE",
                value=(60, 1),
                help="自动撤回，参1：延迟撤回KIMI_AI时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
                default_value=(0, 1),
                type=Tuple[int, int],
            ),
        ],
    ).dict(),
)

video = on_regex("^(\d?)连?(sp|视频|来点视频|video)$", priority=5, block=True)

# url = "https://v.api.aa1.cn/api/api-dy-girl/index.php?aa1=ajdu987hrjfw"
url = "http://api.qemao.com/api/douyin/"


@video.handle()
async def send_video(bot: Bot, event: Event, state: T_State, reg_group: Tuple[Any, ...] = RegexGroup()):
    num = reg_group[0] or 1
    for _ in range(int(num)):
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
