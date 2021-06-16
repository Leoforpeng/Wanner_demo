# -*- coding: utf-8 -*-
# @Time : 2021/4/15 17:24
# @Author : qiu jiahang
import ctypes
import os
from ctypes import *
import sys
from ctypes.wintypes import DWORD, UINT, CHAR
from ctypes.wintypes import WORD
from ctypes.wintypes import LONG
from ctypes.wintypes import BYTE

# 报警信息列表，报一次在回调中加1次记录
alarm_info = []
fun_ctype = WINFUNCTYPE  # 指针函数类型

if 'linux' in sys.platform:
    fun_ctype = CFUNCTYPE


# 设备参数结构体 V30
class NET_DVR_DEVICEINFO_V30(ctypes.Structure):
    _fields_ = [
        ("sSerialNumber", ctypes.c_byte * 48),  # 序列号
        ("byAlarmInPortNum", ctypes.c_byte),  # 模拟报警输入个数
        ("byAlarmOutPortNum", ctypes.c_byte),  # 模拟报警输出个数
        ("byDiskNum", ctypes.c_byte),  # 硬盘个数
        ("byDVRType", ctypes.c_byte),  # 设备类型
        ("byChanNum", ctypes.c_byte),  # 设备模拟通道个数，数字（IP）通道最大个数为byIPChanNum + byHighDChanNum*256
        ("byStartChan", ctypes.c_byte),  # 模拟通道的起始通道号，从1开始。数字通道的起始通道号见下面参数byStartDChan
        ("byAudioChanNum", ctypes.c_byte),  # 设备语音对讲通道数
        ("byIPChanNum", ctypes.c_byte),  # 设备最大数字通道个数，低8位，高8位见byHighDChanNum
        ("byZeroChanNum", ctypes.c_byte),  # 零通道编码个数
        ("byMainProto", ctypes.c_byte),  # 主码流传输协议类型：0- private，1- rtsp，2- 同时支持私有协议和rtsp协议取流（默认采用私有协议取流）
        ("bySubProto", ctypes.c_byte),  # 子码流传输协议类型：0- private，1- rtsp，2- 同时支持私有协议和rtsp协议取流（默认采用私有协议取流）
        ("bySupport", ctypes.c_byte),  # 能力，位与结果为0表示不支持，1表示支持
        # bySupport & 0x1，表示是否支持智能搜索
        # bySupport & 0x2，表示是否支持备份
        # bySupport & 0x4，表示是否支持压缩参数能力获取
        # bySupport & 0x8, 表示是否支持双网卡
        # bySupport & 0x10, 表示支持远程SADP
        # bySupport & 0x20, 表示支持Raid卡功能
        # bySupport & 0x40, 表示支持IPSAN目录查找
        # bySupport & 0x80, 表示支持rtp over rtsp
        ("bySupport1", ctypes.c_byte),  # 能力集扩充，位与结果为0表示不支持，1表示支持
        # bySupport1 & 0x1, 表示是否支持snmp v30
        # bySupport1 & 0x2, 表示是否支持区分回放和下载
        # bySupport1 & 0x4, 表示是否支持布防优先级
        # bySupport1 & 0x8, 表示智能设备是否支持布防时间段扩展
        # bySupport1 & 0x10,表示是否支持多磁盘数（超过33个）
        # bySupport1 & 0x20,表示是否支持rtsp over http
        # bySupport1 & 0x80,表示是否支持车牌新报警信息，且还表示是否支持NET_DVR_IPPARACFG_V40配置
        ("bySupport2", ctypes.c_byte),  # 能力集扩充，位与结果为0表示不支持，1表示支持
        # bySupport2 & 0x1, 表示解码器是否支持通过URL取流解码
        # bySupport2 & 0x2, 表示是否支持FTPV40
        # bySupport2 & 0x4, 表示是否支持ANR(断网录像)
        # bySupport2 & 0x20, 表示是否支持单独获取设备状态子项
        # bySupport2 & 0x40, 表示是否是码流加密设备
        ("wDevType", ctypes.c_uint16),  # 设备型号，详见下文列表
        ("bySupport3", ctypes.c_byte),  # 能力集扩展，位与结果：0- 不支持，1- 支持
        # bySupport3 & 0x1, 表示是否支持多码流
        # bySupport3 & 0x4, 表示是否支持按组配置，具体包含通道图像参数、报警输入参数、IP报警输入/输出接入参数、用户参数、设备工作状态、JPEG抓图、定时和时间抓图、硬盘盘组管理等
        # bySupport3 & 0x20, 表示是否支持通过DDNS域名解析取流
        ("byMultiStreamProto", ctypes.c_byte),  # 是否支持多码流，按位表示，位与结果：0-不支持，1-支持
        # byMultiStreamProto & 0x1, 表示是否支持码流3
        # byMultiStreamProto & 0x2, 表示是否支持码流4
        # byMultiStreamProto & 0x40,表示是否支持主码流
        # byMultiStreamProto & 0x80,表示是否支持子码流
        ("byStartDChan", ctypes.c_byte),  # 起始数字通道号，0表示无数字通道，比如DVR或IPC
        ("byStartDTalkChan", ctypes.c_byte),  # 起始数字对讲通道号，区别于模拟对讲通道号，0表示无数字对讲通道
        ("byHighDChanNum", ctypes.c_byte),  # 数字通道个数，高8位
        ("bySupport4", ctypes.c_byte),  # 能力集扩展，按位表示，位与结果：0- 不支持，1- 支持
        # bySupport4 & 0x01, 表示是否所有码流类型同时支持RTSP和私有协议
        # bySupport4 & 0x10, 表示是否支持域名方式挂载网络硬盘
        ("byLanguageType", ctypes.c_byte),  # 支持语种能力，按位表示，位与结果：0- 不支持，1- 支持
        # byLanguageType ==0，表示老设备，不支持该字段
        # byLanguageType & 0x1，表示是否支持中文
        # byLanguageType & 0x2，表示是否支持英文
        ("byVoiceInChanNum", ctypes.c_byte),  # 音频输入通道数
        ("byStartVoiceInChanNo", ctypes.c_byte),  # 音频输入起始通道号，0表示无效
        ("byRes3", ctypes.c_byte * 2),  # 保留，置为0
        ("byMirrorChanNum", ctypes.c_byte),  # 镜像通道个数，录播主机中用于表示导播通道
        ("wStartMirrorChanNo", ctypes.c_uint16),  # 起始镜像通道号
        ("byRes2", ctypes.c_byte * 2)]  # 保留，置为0
LPNET_DVR_DEVICEINFO_V30 = POINTER(NET_DVR_DEVICEINFO_V30)


# 设备参数结构体 V40
class NET_DVR_DEVICEINFO_V40(ctypes.Structure):
    _fields_ = [
        ('struDeviceV30', NET_DVR_DEVICEINFO_V30),
        ('bySupportLock', BYTE),
        ('byRetryLoginTime', BYTE),
        ('byPasswordLevel', BYTE),
        ('byProxyType', BYTE),
        ('dwSurplusLockTime', DWORD),
        ('byCharEncodeType', BYTE),
        ('bySupportDev5', BYTE),
        ('byLoginMode', BYTE),
        ('byRes2', BYTE * 253)]  # 保留，置为0
LPNET_DVR_DEVICEINFO_V40 = POINTER(NET_DVR_DEVICEINFO_V40)


# 报警设备信息结构体
class NET_DVR_ALARMER(Structure):
    _fields_ = [
        ("byUserIDValid", BYTE),  # userid是否有效 0-无效，1-有效
        ("bySerialValid", BYTE),  # 序列号是否有效 0-无效，1-有效
        ("byVersionValid", BYTE),  # 版本号是否有效 0-无效，1-有效
        ("byDeviceNameValid", BYTE),  # 设备名字是否有效 0-无效，1-有效
        ("byMacAddrValid", BYTE),  # MAC地址是否有效 0-无效，1-有效
        ("byLinkPortValid", BYTE),  # login端口是否有效 0-无效，1-有效
        ("byDeviceIPValid", BYTE),  # 设备IP是否有效 0-无效，1-有效
        ("bySocketIPValid", BYTE),  # socket ip是否有效 0-无效，1-有效
        ("lUserID", LONG),  # NET_DVR_Login()返回值, 布防时有效
        ("sSerialNumber", BYTE * 48),  # 序列号
        ("dwDeviceVersion", DWORD),  # 版本信息 高16位表示主版本，低16位表示次版本
        ("sDeviceName", c_char * 32),  # 设备名字
        ("byMacAddr", BYTE * 6),  # MAC地址
        ("wLinkPort", WORD),  # link port
        ("sDeviceIP", BYTE * 128),  # IP地址
        ("sSocketIP", c_char * 128),  # 报警主动上传时的socket IP地址
        ("byIpProtocol", BYTE),  # Ip协议 0-IPV4, 1-IPV6
        ("byRes2", BYTE * 11)]
LPNET_DVR_ALARMER = POINTER(NET_DVR_ALARMER)


# 报警布防参数结构体
class NET_DVR_SETUPALARM_PARAM(Structure):
    _fields_ = [
        ("dwSize", DWORD),  # 结构体大小
        ("byLevel", BYTE),  # 布防优先级：0- 一等级（高），1- 二等级（中），2- 三等级（低）
        ("byAlarmInfoType", BYTE),
        # 上传报警信息类型（抓拍机支持），0-老报警信息（NET_DVR_PLATE_RESULT），1-新报警信息(NET_ITS_PLATE_RESULT)2012-9-28
        ("byRetAlarmTypeV40", BYTE),
        # 0--返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO, 1--设备支持NET_DVR_ALARMINFO_V40则返回NET_DVR_ALARMINFO_V40，不支持则返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO
        ("byRetDevInfoVersion", BYTE),  # CVR上传报警信息回调结构体版本号 0-COMM_ALARM_DEVICE， 1-COMM_ALARM_DEVICE_V40
        ("byRetVQDAlarmType", BYTE),  # VQD报警上传类型，0-上传报报警NET_DVR_VQD_DIAGNOSE_INFO，1-上传报警NET_DVR_VQD_ALARM
        ("byFaceAlarmDetection", BYTE),
        ("bySupport", BYTE),
        ("byBrokenNetHttp", BYTE),
        ("wTaskNo", WORD),
        # 任务处理号 和 (上传数据NET_DVR_VEHICLE_RECOG_RESULT中的字段dwTaskNo对应 同时 下发任务结构 NET_DVR_VEHICLE_RECOG_COND中的字段dwTaskNo对应)
        ("byDeployType", BYTE),  # 布防类型：0-客户端布防，1-实时布防
        ("byRes1", BYTE * 3),
        ("byAlarmTypeURL", BYTE),
        # bit0-表示人脸抓拍报警上传（INTER_FACESNAP_RESULT）；0-表示二进制传输，1-表示URL传输（设备支持的情况下，设备支持能力根据具体报警能力集判断,同时设备需要支持URL的相关服务，当前是”云存储“）
        ("byCustomCtrl", BYTE)]  # Bit0- 表示支持副驾驶人脸子图上传: 0-不上传,1-上传,(注：只在公司内部8600/8200等平台开放)
LPNET_DVR_SETUPALARM_PARAM = POINTER(NET_DVR_SETUPALARM_PARAM)
fLoginResultCallBack = CFUNCTYPE(None, LONG, DWORD, LPNET_DVR_DEVICEINFO_V30, c_void_p)


# NET_DVR_Login_V40()参数
class NET_DVR_USER_LOGIN_INFO(Structure):
    _fields_ = [
        ("sDeviceAddress", c_char * 129),  # 设备地址，IP 或者普通域名
        ("byUseTransport", BYTE),  # 是否启用能力集透传：0- 不启用透传，默认；1- 启用透传
        ("wPort", WORD),  # 设备端口号，例如：8000
        ("sUserName", c_char * 64),  # 登录用户名，例如：admin
        ("sPassword", c_char * 64),  # 登录密码，例如：12345
        ("cbLoginResult", fLoginResultCallBack),  # 登录状态回调函数，bUseAsynLogin 为1时有效
        ("pUser", c_void_p),  # 用户数据
        ("bUseAsynLogin", c_int),  # 是否异步登录：0- 否，1- 是
        ("byProxyType", BYTE),  # 0:不使用代理，1：使用标准代理，2：使用EHome代理
        ("byUseUTCTime", BYTE),
        # 0-不进行转换，默认,1-接口上输入输出全部使用UTC时间,SDK完成UTC时间与设备时区的转换,2-接口上输入输出全部使用平台本地时间，SDK完成平台本地时间与设备时区的转换
        ("byLoginMode", BYTE),  # 0-Private 1-ISAPI 2-自适应
        ("byHttps", BYTE),  # 0-不适用tls，1-使用tls 2-自适应
        ("iProxyID", LONG),  # 代理服务器序号，添加代理服务器信息时，相对应的服务器数组下表值
        ("byVerifyMode", LONG),  # 认证方式，0-不认证，1-双向认证，2-单向认证；认证仅在使用TLS的时候生效;
        ("byRes2", BYTE * 119)]
LPNET_DVR_USER_LOGIN_INFO = POINTER(NET_DVR_USER_LOGIN_INFO)


# 上传的报警信息结构体。
class NET_DVR_ALARMINFO_V30(Structure):
    _fields_ = [
        ("dwAlarmType", DWORD),  # 报警类型
        ("dwAlarmInputNumber", DWORD),  # 报警输入端口，当报警类型为0、23时有效
        ("byAlarmOutputNumber", BYTE * 96),
        # 触发的报警输出端口，值为1表示该报警端口输出，如byAlarmOutputNumber[0]=1表示触发第1个报警输出口输出，byAlarmOutputNumber[1]=1表示触发第2个报警输出口，依次类推
        ("byAlarmRelateChannel", BYTE * 64),  # 触发的录像通道，值为1表示该通道录像，如byAlarmRelateChannel[0]=1表示触发第1个通道录像
        ("byChannel", BYTE * 64),  # 发生报警的通道。当报警类型为2、3、6、9、10、11、13、15、16时有效，如byChannel[0]=1表示第1个通道报警
        ("byDiskNumber", BYTE * 33)]  # 发生报警的硬盘。当报警类型为1，4，5时有效，byDiskNumber[0]=1表示1号硬盘异常
LPNET_DVR_ALARMINFO_V30 = POINTER(NET_DVR_ALARMINFO_V30)


# 报警布防参数结构体
class NET_DVR_SETUPALARM_PARAM(Structure):
    _fields_ = [
        ("dwSize", DWORD),  # 结构体大小
        ("byLevel", BYTE),  # 布防优先级：0- 一等级（高），1- 二等级（中），2- 三等级（低）
        ("byAlarmInfoType", BYTE),
        # 上传报警信息类型（抓拍机支持），0-老报警信息（NET_DVR_PLATE_RESULT），1-新报警信息(NET_ITS_PLATE_RESULT)2012-9-28
        ("byRetAlarmTypeV40", BYTE),
        # 0--返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO, 1--设备支持NET_DVR_ALARMINFO_V40则返回NET_DVR_ALARMINFO_V40，不支持则返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO
        ("byRetDevInfoVersion", BYTE),  # CVR上传报警信息回调结构体版本号 0-COMM_ALARM_DEVICE， 1-COMM_ALARM_DEVICE_V40
        ("byRetVQDAlarmType", BYTE),  # VQD报警上传类型，0-上传报报警NET_DVR_VQD_DIAGNOSE_INFO，1-上传报警NET_DVR_VQD_ALARM
        ("byFaceAlarmDetection", BYTE),
        ("bySupport", BYTE),
        ("byBrokenNetHttp", BYTE),
        ("wTaskNo", WORD),
        # 任务处理号 和 (上传数据NET_DVR_VEHICLE_RECOG_RESULT中的字段dwTaskNo对应 同时 下发任务结构 NET_DVR_VEHICLE_RECOG_COND中的字段dwTaskNo对应)
        ("byDeployType", BYTE),  # 布防类型：0-客户端布防，1-实时布防
        ("byRes1", BYTE * 3),
        ("byAlarmTypeURL", BYTE),
        # bit0-表示人脸抓拍报警上传（INTER_FACESNAP_RESULT）；0-表示二进制传输，1-表示URL传输（设备支持的情况下，设备支持能力根据具体报警能力集判断,同时设备需要支持URL的相关服务，当前是”云存储“）
        ("byCustomCtrl", BYTE)] # Bit0- 表示支持副驾驶人脸子图上传: 0-不上传,1-上传,(注：只在公司内部8600/8200等平台开放)
LPNET_DVR_SETUPALARM_PARAM = POINTER(NET_DVR_SETUPALARM_PARAM)


# 时间参数结构体
class NET_DVR_TIME(Structure):
    _fields_ = [
        ("dwYear", c_ulong),  # 年
        ("dwMonth", c_ulong),  # 月
        ("dwDay", c_ulong),  # 日
        ("dwHour", c_ulong),  # 时
        ("dwMinute", c_ulong),  # 分
        ("dwSecond", c_ulong)]  # 秒
LPNET_DVR_TIME = POINTER(NET_DVR_TIME)


# IP地址结构体
class NET_DVR_IPADDR(Structure):
    _fields_ = [
        ("sIpV4", CHAR * 16),  # 设备IPv4地址
        ("sIpV6", BYTE * 128)]  # 设备IPv6地址
LPNET_DVR_IPADDR = POINTER(NET_DVR_IPADDR)


# 门禁主机事件信息
class NET_DVR_ACS_EVENT_INFO(Structure):
    _fields_ = [
        ("dwSize", c_ulong),  # 结构体大小
        ("byCardNo", BYTE * 32),  # 卡号
        ("byCardType", BYTE),  # 卡类型：1- 普通卡，2- 残障人士卡，3- 黑名单卡，4- 巡更卡，5- 胁迫卡，6- 超级卡，7- 来宾卡，8- 解除卡，为0表示无效
        ("byAllowListNo", BYTE),  # 白名单单号，取值范围：1~8，0表示无效
        ("byReportChannel", BYTE),  # 报告上传通道：1- 布防上传，2- 中心组1上传，3- 中心组2上传，0表示无效
        ("byCardReaderKind", BYTE),  # 读卡器类型：0- 无效，1- IC读卡器，2- 身份证读卡器，3- 二维码读卡器，4- 指纹头
        ("dwCardReaderNo", c_ulong),  # 读卡器编号，为0表示无效
        ("dwDoorNo", c_ulong),  # 门编号（或者梯控的楼层编号），为0表示无效（当接的设备为人员通道设备时，门1为进方向，门2为出方向）
        ("dwVerifyNo", c_ulong),  # 多重卡认证序号，为0表示无效
        ("dwAlarmInNo", c_ulong),  # 报警输入号，为0表示无效
        ("dwAlarmOutNo", c_ulong),  # 报警输出号，为0表示无效
        ("dwCaseSensorNo", c_ulong),  # 事件触发器编号
        ("dwRs485No", c_ulong),  # RS485通道号，为0表示无效
        ("dwMultiCardGroupNo", c_ulong),  # 群组编号
        ("wAccessChannel", WORD),  # 人员通道号
        ("byDeviceNo", BYTE),  # 设备编号，为0表示无效
        ("byDistractControlNo", BYTE),  # 分控器编号，为0表示无效
        ("dwEmployeeNo", c_ulong),  # 工号，为0无效
        ("wLocalControllerID", WORD),  # 就地控制器编号，0-门禁主机，1-255代表就地控制器
        ("byInternetAccess", BYTE),  # 网口ID：（1-上行网口1,2-上行网口2,3-下行网口1）
        ("byType", BYTE),
        # 防区类型，0:即时防区,1-24小时防区,2-延时防区,3-内部防区,4-钥匙防区,5-火警防区,6-周界防区,7-24小时无声防区,8-24小时辅助防区,9-24小时震动防区,10-门禁紧急开门防区,11-门禁紧急关门防区，0xff-无
        ("byMACAddr", BYTE * 6),  # 物理地址，为0无效
        ("bySwipeCardType", BYTE),  # 刷卡类型，0-无效，1-二维码
        ("byMask", BYTE),  # 是否带口罩：0-保留，1-未知，2-不戴口罩，3-戴口罩
        ("dwSerialNo", c_ulong),  # 事件流水号，为0无效
        ("byChannelControllerID", BYTE),  # 通道控制器ID，为0无效，1-主通道控制器，2-从通道控制器
        ("byChannelControllerLampID", BYTE),  # 通道控制器灯板ID，为0无效（有效范围1-255）
        ("byChannelControllerIRAdaptorID", BYTE),  # 通道控制器红外转接板ID，为0无效（有效范围1-255）
        ("byChannelControllerIREmitterID", BYTE),  # 通道控制器红外对射ID，为0无效（有效范围1-255）
        ("byHelmet", BYTE),  # 可选，是否戴安全帽：0-保留，1-未知，2-不戴安全, 3-戴安全帽
        ("byRes", BYTE * 3)]  # 保留，置为0
LPNET_DVR_ACS_EVENT_INFO = POINTER(NET_DVR_ACS_EVENT_INFO)


# 门禁主机报警信息结构体
class NET_DVR_ACS_ALARM_INFO(Structure):
    _fields_ = [
        ("dwSize", c_ulong),  # 结构体大小
        ("dwMajor", c_ulong),  # 报警主类型，具体定义见“Remarks”说明
        ("dwMinor", c_ulong),  # 报警次类型，次类型含义根据主类型不同而不同，具体定义见“Remarks”说明
        ("struTime", NET_DVR_TIME),  # 报警时间
        ("sNetUser", BYTE * 16),  # 网络操作的用户名
        ("struRemoteHostAddr", NET_DVR_IPADDR),  # 远程主机地址
        ("struAcsEventInfo", NET_DVR_ACS_EVENT_INFO),  # 报警信息详细参数
        ("dwPicDataLen", c_ulong),  # 图片数据大小，不为0是表示后面带数据
        ("pPicData", c_char_p),  # 图片数据缓冲区
        ("wInductiveEventType", WORD),  # 归纳事件类型，0-无效，客户端判断该值为非0值后，报警类型通过归纳事件类型区分，否则通过原有报警主次类型（dwMajor、dwMinor）区分
        ("byPicTransType", BYTE),  # 图片数据传输方式: 0-二进制；1-url
        ("byRes1", BYTE),  # 保留，置为0
        ("dwIOTChannelNo", c_ulong),  # IOT通道号
        ("pAcsEventInfoExtend", c_char_p),  # byAcsEventInfoExtend为1时，表示指向一个NET_DVR_ACS_EVENT_INFO_EXTEND结构体
        ("byAcsEventInfoExtend", BYTE),  # pAcsEventInfoExtend是否有效：0-无效，1-有效
        ("byTimeType", BYTE),  # 时间类型：0-设备本地时间，1-UTC时间（struTime的时间）
        ("byRes2", BYTE),  # 保留，置为0
        ("byAcsEventInfoExtendV20", BYTE),  # pAcsEventInfoExtendV20是否有效：0-无效，1-有效
        ("pAcsEventInfoExtendV20", c_char_p),  # byAcsEventInfoExtendV20为1时，表示指向一个NET_DVR_ACS_EVENT_INFO_EXTEND_V20结构体
        ("byRes", BYTE * 4)]  # 保留，置为0
LPNET_DVR_ACS_ALARM_INFO = POINTER(NET_DVR_ACS_ALARM_INFO)

MSGCallBack = fun_ctype(c_bool, LONG, LPNET_DVR_ALARMER, c_void_p, c_ulong, c_void_p)


def g_fMessageCallBack_Alarm(lCommand, pAlarmer, pAlarmInfo, dwBufLen, pUser):
    """
    解析报警信息
    """
    global alarm_info
    Alarmer = pAlarmer.contents  # 取指针指向的结构体
    single_alrm = {}
    seriel_num = ''
    for n in Alarmer.sSerialNumber[0:48]:
        if n != 0:
            seriel_num += chr(n)
    single_alrm['设备序列号sSerialNumber'] = seriel_num
    if Alarmer.byUserIDValid:
        single_alrm['lUserID'] = Alarmer.lUserID

    # 移动侦测、视频丢失、遮挡、IO信号量等报警信息(V3.0以上版本支持的设备)
    if lCommand == 0x4000:
        print('移动侦测')
        Alarm_struct = cast(pAlarmInfo,
                            LPNET_DVR_ALARMINFO_V30).contents  # 当lCommand是COMM_ALARM时将pAlarmInfo强制转换为NET_DVR_ALARMINFO类型的指针再取值
        single_alrm['dwAlarmType'] = hex(Alarm_struct.dwAlarmType)
        single_alrm['byAlarmOutputNumber'] = Alarm_struct.byAlarmOutputNumber[0]
        single_alrm['byChannel'] = Alarm_struct.byChannel[0]

    if lCommand == 0x5002:
        print('门禁触发报警')
        Alarm_struct = cast(pAlarmInfo,
                            LPNET_DVR_ACS_ALARM_INFO).contents  # 当lCommand是0x5002时将pAlarmInfo强制转换为NET_DVR_ACS_ALARM_INFO类型的指针再取值
        single_alrm['dwSize'] = Alarm_struct.dwSize
        single_alrm['dwMajor'] = hex(Alarm_struct.dwMajor)
        single_alrm['dwMinor'] = hex(Alarm_struct.dwMinor)
        single_alrm['struTime'] = Alarm_struct.struTime.dwYear
        localtime = time.asctime(time.localtime(time.time()))
        single_alrm['localtime'] = localtime

    alarm_info.append(single_alrm)
    print(alarm_info[-1])



setdvrmsg_callback_func = MSGCallBack(g_fMessageCallBack_Alarm)

if __name__ == '__main__':
    # 加载库,先加载依赖库
    os.chdir(r'.设备序列号sSerialNumber/core/')
    sdk = ctypes.CDLL(r'./HCNetSDK.dll')
    WinDLL('./HCCore.dll', RTLD_GLOBAL)

    # 初始化
    sdk.NET_DVR_Init()
    # 设置连接时间和重连时间
    sdk.NET_DVR_SetConnectTime(2000, 1)
    sdk.NET_DVR_SetReconnect(10000, 1)
    sdk.NET_DVR_SetDVRMessageCallBack_V31(setdvrmsg_callback_func, None)
    # 初始化用户id, 在调用正常是程序一般返回正数，故初始化一个负数
    UserID = c_long(-1)

    # 用户注册设备
    # c++传递进去的是byte型数据，需要转成byte型传进去，否则会乱码
    # 登录参数，包括设备地址、登录用户、密码等
    struLoginInfo = NET_DVR_USER_LOGIN_INFO()
    struLoginInfo.bUseAsynLogin = 0  # 同步登录方式
    struLoginInfo.sDeviceAddress = bytes("10.10.5.8", "ascii")  # 设备IP地址
    struLoginInfo.wPort = 8000  # 设备服务端口
    struLoginInfo.sUserName = bytes("admin", "ascii")  # 设备登录用户名
    struLoginInfo.sPassword = bytes("tycon1588", "ascii")  # 设备登录密码

    # 设备信息, 输出参数
    struDeviceInfoV40 = NET_DVR_DEVICEINFO_V40()
    sdk.NET_DVR_Login_V40.restype = c_long
    sdk.NET_DVR_GetLastError.restype = c_uint
    UserID = sdk.NET_DVR_Login_V40(byref(struLoginInfo), byref(struDeviceInfoV40))
    if UserID < 0:
        print("Login failed, error code: %s", sdk.NET_DVR_GetLastError())
        sdk.NET_DVR_Cleanup()
    else:
        print('登录成功，device_num：%s' % str(struDeviceInfoV40.struDeviceV30.sSerialNumber))

    # 布防句柄
    handle = c_long(-1)
    sdk.NET_DVR_SetupAlarmChan_V41.restype = c_long

    # 启用布防
    struAlarmParam = NET_DVR_SETUPALARM_PARAM()
    struAlarmParam.dwSize = sizeof(struAlarmParam)
    struAlarmParam.byAlarmInfoType = 1  # 智能交通报警信息上传类型：0- 老报警信息（NET_DVR_PLATE_RESULT），1- 新报警信息(NET_ITS_PLATE_RESULT)
    struAlarmParam.byDeployType = 1
    handle = sdk.NET_DVR_SetupAlarmChan_V41(UserID, byref(struAlarmParam))
    if handle < 0:
        print("NET_DVR_SetupAlarmChan_V41 失败, error code: %s", sdk.NET_DVR_GetLastError())
        sdk.NET_DVR_Logout(UserID)
        sdk.NET_DVR_Cleanup()

    import time
    time_flag = 0
    # global alarm_info
    while time_flag < 60:
        print('waite alarm ... %s' % time_flag)
        time_flag += 1
        time.sleep(100)
        if alarm_info:
            print('alarm_info=%s' % str(alarm_info))
            break
    # 撤销布防
    sdk.NET_DVR_CloseAlarmChan_V30(handle)
    # 注销用户
    sdk.NET_DVR_Logout(UserID)
    # 释放SDK资源
    sdk.NET_DVR_Cleanup()
