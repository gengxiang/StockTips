# coding=gbk
import time

import yaml
from wxauto import *

from gengxiang.code.getAll import get_mysql

wx = WeChat()  # 获取当前微信客户端
who = "G.X"  # 要发送的人
todayStr = time.strftime('%Y-%m-%d', time.localtime(time.time()))


def yaml_load():
    f = open('../resource/conf.yaml')
    data = yaml.load(f.read(), Loader=yaml.FullLoader)
    print(type(data))


def send_wechat(msg):
    WxUtils.SetClipboard(msg)
    wx.ChatWith(who)
    wx.SendClipboard(who)
    # wx.ChatWith(who)
    # wx.SendMsg(msg, who)


def send_wechat_thsbks(thsBsk_list):
    if len(thsBsk_list) == 0:
        return
    wx.ChatWith(who)
    msg = todayStr + "同花顺板块信息："
    for bsk in thsBsk_list:
        msg = msg + "\n " + '#' + bsk['行业名称'] + "  +>领涨股: '#'" + str(
            bsk['领涨股']) + " ->净流入资金(亿): " + str(bsk['净流入资金(亿)'])
    send_wechat(msg)
    print("发送结束！")


def send_wechat_bks(bsk_list):
    if len(bsk_list) == 0:
        return
    wx.ChatWith(who)
    msg = todayStr + "东方财富板块信息："
    for bsk in bsk_list:
        msg = msg + "\n " + '#' + bsk['name'] + " ->" + str(bsk['板块列表'])
    send_wechat(msg)
    print("发送结束！")


def send_wechat_tips(total_amo, review_url):
    dot = calc_reasonable_position2(total_amo)
    cha_value1 = total_amo[0] - total_amo[1]
    cha_value2 = total_amo[1] - total_amo[0]
    if total_amo[0] >= total_amo[1]:
        msg = todayStr + "\n" + "两市成交额：" + str(total_amo[0] / 10000) + "亿\n" + "放量：" + str(
            cha_value1 / 10000) + "亿\n" \
              + "操作建议：" + dot[2]["操作建议"] + "\n" + "最大仓位：" + dot[2]["建议仓位区间"]
        send_wechat(msg)
    if total_amo[0] < total_amo[1]:
        msg = todayStr + "\n" + "两市成交额：" + str(total_amo[0] / 10000) + "亿\n" + "缩量量：" + str(
            cha_value2 / 10000) + "亿\n" \
              + "操作建议：" + dot[2]["操作建议"] + "\n" + "最大仓位：" + str(dot[2]["建议仓位区间"])
        send_wechat(msg)

    # focus = "近5日焦点复盘地址：\n"
    # i = 0
    # for review in review_url:
    #     i += 1
    #     if i < 5:
    #         focus = focus + review + " \n"
    # send_wechat(focus)


def volume_based_position_analysis(current, yesterday, ma5, ma16):
    """量价单维度打分，兼容旧结构key"""
    ma5 = ma5 if ma5 != 0 else 1e-9
    ma16 = ma16 if ma16 != 1e-9 else 1e-9
    current = max(current, 1e-9)

    ratio_5 = current / ma5
    ratio_16 = current / ma16
    raw_score = ratio_5 * 30 + ratio_16 * 20
    dim_score = max(0, min(100, raw_score))

    return {
        "综合评分": round(dim_score, 1),
        "当日值": round(current, 2),
        "昨日值": round(yesterday, 2),
        "5周期均值": round(ma5, 2),
        "16周期均值": round(ma16, 2)
    }


def calc_reasonable_position2(total_amo, ma16_weak=False, ma16_top=False, ma16_bottom=False):
    """
    多空分级严格风控：下跌逐级限仓，放量突破均线逐级放开加仓
    新增能力：
        1. 短期量价反转识别（连续缩量转跌/连续放量转涨）
        2. 中期16日均线趋势拐点识别（涨转跌见顶/跌转涨见底）
        3. MA16长期持续向下弱势空仓强制约束
        4. 底部固定全套交易纪律输出
    入参说明：
        total_amo: [今日成交额,昨日成交额,5日均额,16日均额,30日均额,今日价,昨日价,5日均价,16日均价,30日均价]
        ma16_weak: bool MA16连续向下，长期弱势环境
        ma16_top: bool MA16由涨转跌（中期见顶拐点）
        ma16_bottom: bool MA16由跌转涨（中期见底拐点）
    :return: price_result, volume_result, 结果字典
    """
    # 拆分行情数据
    vol_today, vol_yest, vol_ma5, vol_ma16, vol_ma30 = total_amo[0:5]
    price_today, price_yest, price_ma5, price_ma16, price_ma30 = total_amo[5:10]

    # 量价打分
    price_result = volume_based_position_analysis(price_today, price_yest, price_ma5, price_ma16)
    volume_result = volume_based_position_analysis(vol_today, vol_yest, vol_ma5, vol_ma16)
    price_score = price_result["综合评分"]
    volume_score = volume_result["综合评分"]

    # 单日放量标记：今日成交额大于5日均额
    is_volume_spike = vol_today > vol_ma5

    # ========== 短期量价拐点（原有逻辑） ==========
    # 多头短期转跌预警：连续两日缩量 + 现价跌破5日线
    turn_bear_warn = (vol_today < vol_ma5) and (vol_yest < vol_ma5) and (price_today < price_ma5)
    # 底部短期企稳信号：连续两日放量 + 现价站上5日线
    turn_bull_signal = (vol_today > vol_ma5) and (vol_yest > vol_ma5) and (price_today > price_ma5)

    # ========== 中期MA16均线拐点（新增外部传入趋势标记） ==========
    mid_trend_tip = ""
    mid_trend_risk = ""
    if ma16_top:
        mid_trend_tip = "【中期预警：16日均线由涨转跌，中期上涨趋势见顶，分批减仓】"
        mid_trend_risk = "中期均线拐头向下，回调风险放大，仓位上限强制下调"
    if ma16_bottom:
        mid_trend_tip = "【中期机会：16日均线由跌转涨，中期下跌趋势见底，可分批低吸】"
    if ma16_weak:
        mid_trend_tip = "【长期弱势：16日均线持续向下，大环境空头，优先空仓观望】"
        mid_trend_risk = "长期均线弱势，禁止重仓参与反弹"

    # 趋势变量初始化
    trend_type = "震荡整理"
    max_allow_pos = 1.0
    risk_notice = ""
    w_price, w_volume = 0.4, 0.6
    turn_tip = ""  # 短期量价反转提示文案

    # ===================== 多头分级（现价站上5日线） =====================
    if price_today > price_ma5:
        # 二阶强多头：5日线站上16日线，多头排列
        if price_ma5 > price_ma16:
            trend_type = "二阶多头：放量站稳16日线，积极加仓区" if is_volume_spike else "二阶多头：无量站上16日线"
            max_allow_pos = 1.0
            w_price, w_volume = 0.4, 0.6
            turn_tip = "【多头纪律：趋势完好耐心持股，不要小幅盈利频繁止盈踏空主升】"

            # 短期缩量破5日线预警 → 降仓
            if turn_bear_warn:
                max_allow_pos = 0.6
                risk_notice = "短期警告：连续两日成交额萎缩+跌破5日线，上涨趋势短期拐头风险，大幅降仓规避回调！"
            # 叠加中期均线见顶拐点，进一步压缩仓位
            if ma16_top:
                max_allow_pos = min(max_allow_pos, 0.4)
                risk_notice += "；中期16日均线拐头向下，双重风险，严格控仓"
            # 长期弱势环境直接限制最高半仓
            if ma16_weak:
                max_allow_pos = min(max_allow_pos, 0.5)
                risk_notice += "；大周期均线弱势，反弹空间有限，不适合重仓"
        else:
            # 一阶突破：仅突破5日线，未站上16日线
            trend_type = "一阶突破：放量突破5日线，适度加仓区" if is_volume_spike else "一阶突破：无量站上5日线"
            max_allow_pos = 0.8
            w_price, w_volume = 0.4, 0.6
            turn_tip = ""

            if turn_bear_warn:
                max_allow_pos = 0.4
                risk_notice = "短期警告：连续缩量走弱，反弹大概率结束，严控仓位不追加买入"
            if ma16_top:
                max_allow_pos = min(max_allow_pos, 0.3)
                risk_notice += "；中期均线见顶，反弹持续性差"
            if ma16_weak:
                max_allow_pos = min(max_allow_pos, 0.3)
                risk_notice += "；长期空头环境，反弹仅适合快进快出"

    else:
        # ===================== 空头分级（现价跌破5日线） =====================
        w_price, w_volume = 0.6, 0.4
        turn_tip = "【空头纪律：所有反弹均逢高兑现，不幻想主升行情，禁止加仓摊薄成本】"

        # 二档空头：5日线跌破16日线，完整空头排列
        if price_ma5 < price_ma16:
            trend_type = "二档空头：均线空头排列，建议空仓观望"
            max_allow_pos = 0.2
            risk_notice = "趋势破位二档空头，常规最高仅允许20%底仓，禁止持仓过重"

            # 短期放量企稳，小幅放宽
            if turn_bull_signal:
                max_allow_pos = 0.35
                risk_notice += "；短期连续放量企稳，可小仓位试错，不可重仓抄底"
            # 中期均线见底拐头，适度提升试错仓位
            if ma16_bottom:
                max_allow_pos = min(max_allow_pos, 0.45)
                risk_notice += "；叠加16日均线跌转涨，中期底部信号，小仓位布局"
            # 长期弱势强制压底仓
            if ma16_weak:
                max_allow_pos = min(max_allow_pos, 0.1)
                risk_notice += "；大周期持续下行，抄底风险极高，尽量空仓"
        # 一档空头：仅现价跌破5日线
        else:
            trend_type = "一档空头：阴线跌破5日线，半仓封顶"
            max_allow_pos = 0.5
            risk_notice = "一档空头跌破5日线，常规仓位上限50%，不可重仓"

            if turn_bull_signal:
                max_allow_pos = 0.65
                risk_notice += "；连续两日放量企稳，短期反弹机会，反弹到位及时离场"
            if ma16_bottom:
                max_allow_pos = min(max_allow_pos, 0.7)
                risk_notice += "；16日均线拐头向上，中期修复行情，反弹空间扩大"
            if ma16_weak:
                max_allow_pos = min(max_allow_pos, 0.3)
                risk_notice += "；长期均线弱势，反弹高度有限"

    # 加权综合得分
    base_score = round(price_score * w_price + volume_score * w_volume, 1)
    final_score = max(0, min(100, base_score))

    # 基础仓位档位
    if final_score >= 90:
        base_level = "重仓"
        base_min, base_max = 0.8, 1.0
    elif final_score >= 70:
        base_level = "中高仓"
        base_min, base_max = 0.6, 0.8
    elif final_score >= 50:
        base_level = "中等仓"
        base_min, base_max = 0.4, 0.6
    elif final_score >= 30:
        base_level = "轻仓"
        base_min, base_max = 0.2, 0.4
    else:
        base_level = "空仓/观望"
        base_min, base_max = 0.0, 0.2

    # 趋势硬性上限截断
    real_max = min(base_max, max_allow_pos)
    real_min = min(base_min, real_max)
    final_position = f"{real_min * 100:.0f}%~{real_max * 100:.0f}%"

    # ===================== 操作建议 =====================
    base_op = ""
    if price_score >= 50 and volume_score >= 50:
        if "二阶多头" in trend_type and is_volume_spike:
            base_op = "买入/持有信号（放量突破16日线多头共振，积极加仓！）"
        elif "一阶突破" in trend_type and is_volume_spike:
            base_op = "买入信号（放量突破5日线，可适度加仓）"
        elif "空头" in trend_type:
            base_op = "观望信号（价量尚可，但处于下跌均线，严控仓位）"
        else:
            base_op = "买入/持有信号（价量共振走强）,想想赚钱的感觉！"
    elif price_score >= 50 and volume_score < 50:
        base_op = "观望信号（价强量弱，无量上涨不宜加仓）"
    elif price_score < 50 and volume_score >= 50:
        base_op = "观望信号（量强价弱，反弹减仓）"
    else:
        base_op = "卖出/空仓信号（价量双弱）, 想想亏钱的日子！"

    # 拼接基础内容
    full_op = f"{base_op}{turn_tip}{mid_trend_tip}"
    if risk_notice:
        operation = f"{full_op}【风险提示：{risk_notice}】"
    else:
        operation = full_op

    # ===================== 固定追加全套交易纪律（新增固定段） =====================
    fixed_rule_text = """
——————统一交易纪律——————
空头纪律：所有反弹均逢高兑现，不幻想主升行情，禁止加仓摊薄成本
多头纪律：趋势完好耐心持股，不要小幅盈利频繁止盈踏空主升
操作纪律；
1.弱势环境赚了就走，不要想着吃一波反弹
2.强势环境勇敢持股，不要怕回调
3、低开超过3%，不能瞬间上拉，要赶紧跑，闸刀来了！
散户心理： 涨了想卖（怕跌，损失厌恶），亏了想抗（怕反弹，损失厌恶）
"""
    # 固定拼接到操作建议末尾
    operation = operation + fixed_rule_text

    # ===================== 返回字典：原版字段全部保留 + 新增均线趋势拐点 =====================
    res_dict = {
        # 原版基础输出
        "最终综合评分": final_score,
        "最终仓位等级": base_level,
        "建议仓位区间": final_position,
        "操作建议": operation,
        "价格评分": price_score,
        "成交量评分": volume_score,
        "价格维度详情": price_result,
        "成交量维度详情": volume_result,

        # 趋势扩展
        "当前趋势档位": trend_type,
        "趋势允许最大仓位": f"{max_allow_pos * 100:.0f}%",
        "是否单日放量": is_volume_spike,
        "动态价量权重": {"价格权重": w_price, "成交量权重": w_volume},
        "均线行情数据": {
            "现价": round(price_today, 2),
            "MA5价格": round(price_ma5, 2),
            "MA16价格": round(price_ma16, 2),
            "当日成交额": vol_today,
            "昨日成交额": vol_yest,
            "5日均成交额": vol_ma5
        },

        # 短期量价拐点
        "短期量价拐点预警": {
            "多头短期转跌(连续缩量破5日线)": turn_bear_warn,
            "底部短期企稳(连续放量站上5日线)": turn_bull_signal
        },
        # 新增中期MA16均线趋势状态
        "中期MA16均线趋势状态": {
            "MA16长期弱势连续向下": ma16_weak,
            "MA16由涨转跌见顶拐点": ma16_top,
            "MA16由跌转涨见底拐点": ma16_bottom
        }
    }

    print("===== 价格维度分析结果 =====", price_result)
    print("===== 成交量维度分析结果 =====", volume_result)
    print("===== 中期16日均线趋势标记 =====", res_dict["中期MA16均线趋势状态"])
    return price_result, volume_result, res_dict


def calc_reasonable_position1(total_amo):
    """
    多空分级严格风控：下跌逐级限仓，放量突破均线逐级放开加仓
    新增：趋势反转灵敏识别【连续3日缩量转跌/连续3日放量转涨，拐点更谨慎】、多空专属持仓纪律提示
    :param total_amo: [今日成交额,昨日成交额,前日成交额,5日均额,16日均额,30日均额,今日价,昨日价,5日均价,16日均价,30日均价]
    :return: price_result, volume_result, 结果字典
    """
    # 拆分行情数据（新增前日成交额 vol_day_before_yest）
    vol_today, vol_yest, vol_day_before_yest, vol_ma5, vol_ma16, vol_ma30 = total_amo[0:6]
    price_today, price_yest, price_ma5, price_ma16, price_ma30 = total_amo[6:11]

    # 量价打分
    price_result = volume_based_position_analysis(price_today, price_yest, price_ma5, price_ma16)
    volume_result = volume_based_position_analysis(vol_today, vol_yest, vol_ma5, vol_ma16)
    price_score = price_result["综合评分"]
    volume_score = volume_result["综合评分"]

    # 单日放量标记：今日成交额大于5日均额
    is_volume_spike = vol_today > vol_ma5

    # ========== 【修改：连续3日判定，拐点更谨慎】 ==========
    # 1. 多头转跌预警：连续3日缩量 + 现价跌破5日线，上涨趋势末端拐头
    turn_bear_warn = (vol_today < vol_ma5) and (vol_yest < vol_ma5) and (vol_day_before_yest < vol_ma5) and (
                price_today < price_ma5)
    # 2. 底部反转企稳：连续3日放量 + 现价站上5日线，下跌趋势见底反弹
    turn_bull_signal = (vol_today > vol_ma5) and (vol_yest > vol_ma5) and (vol_day_before_yest > vol_ma5) and (
                price_today > price_ma5)

    # 趋势变量初始化
    trend_type = "震荡整理"
    max_allow_pos = 1.0
    risk_notice = ""
    w_price, w_volume = 0.4, 0.6
    turn_tip = ""  # 反转专属提示文案

    # ===================== 多头突破分级（上涨放量加仓逻辑） =====================
    if price_today > price_ma5:
        # 二阶强多头：站稳5日线 + 5日线站上16日线，完整多头排列
        if price_ma5 > price_ma16:
            trend_type = "二阶多头：放量站稳16日线，积极加仓区" if is_volume_spike else "二阶多头：无量站上16日线"
            max_allow_pos = 1.0
            w_price, w_volume = 0.4, 0.6
            # 多头基础持仓纪律
            turn_tip = "【多头纪律：趋势完好耐心持股，不要小幅盈利频繁止盈踏空主升】"
            # 多头末尾拐头，反转预警，强制降低仓位上限
            if turn_bear_warn:
                max_allow_pos = 0.6
                risk_notice = "警告：连续三日成交额萎缩+跌破5日线，上涨趋势有拐头风险，大幅降仓规避回调！"
        else:
            # 一阶突破：仅突破5日线，未站上16日线
            trend_type = "一阶突破：放量突破5日线，适度加仓区" if is_volume_spike else "一阶突破：无量站上5日线"
            max_allow_pos = 0.8
            w_price, w_volume = 0.4, 0.6
            turn_tip = ""
            if turn_bear_warn:
                max_allow_pos = 0.4
                risk_notice = "警告：连续三日缩量走弱，反弹大概率结束，严控仓位不追加买入"
    else:
        # ===================== 空头分级（下跌严格限仓） =====================
        w_price, w_volume = 0.6, 0.4
        # 空头统一纪律
        turn_tip = "【空头纪律：所有反弹均逢高兑现，不幻想主升行情，禁止加仓摊薄成本】"
        # 二档空头：跌破5日线 + 5日线跌破16日线，趋势走坏
        if price_ma5 < price_ma16:
            trend_type = "二档空头：均线空头排列，建议空仓观望"
            max_allow_pos = 0.2
            risk_notice = "趋势破位二档空头，最高仅允许20%底仓，禁止持仓过重"
            # 出现连续3日放量企稳拐点，小幅放宽仓位底线
            if turn_bull_signal:
                max_allow_pos = 0.35
                risk_notice += "；连续三日放量企稳信号出现，可小仓位试错，不可重仓抄底"
        # 一档空头：仅现价跌破5日线
        else:
            trend_type = "一档空头：阴线跌破5日线，半仓封顶"
            max_allow_pos = 0.5
            risk_notice = "一档空头跌破5日线，仓位上限50%，不可重仓"
            if turn_bull_signal:
                max_allow_pos = 0.65
                risk_notice += "；连续三日放量企稳，短期反弹机会，反弹到位及时离场"

    # 加权综合得分
    base_score = round(price_score * w_price + volume_score * w_volume, 1)
    final_score = max(0, min(100, base_score))

    # 基础仓位档位（沿用原版分数阈值）
    if final_score >= 90:
        base_level = "重仓"
        base_min, base_max = 0.8, 1.0
    elif final_score >= 70:
        base_level = "中高仓"
        base_min, base_max = 0.6, 0.8
    elif final_score >= 50:
        base_level = "中等仓"
        base_min, base_max = 0.4, 0.6
    elif final_score >= 30:
        base_level = "轻仓"
        base_min, base_max = 0.2, 0.4
    else:
        base_level = "空仓/观望"
        base_min, base_max = 0.0, 0.2

    # 趋势硬性仓位上限截断
    real_max = min(base_max, max_allow_pos)
    real_min = min(base_min, real_max)
    final_position = f"{real_min * 100:.0f}%~{real_max * 100:.0f}%"

    # ===================== 操作建议，区分多空突破信号 =====================
    base_op = ""
    if price_score >= 50 and volume_score >= 50:
        if "二阶多头" in trend_type and is_volume_spike:
            base_op = "买入/持有信号（放量突破16日线多头共振，积极加仓！）"
        elif "一阶突破" in trend_type and is_volume_spike:
            base_op = "买入信号（放量突破5日线，可适度加仓）"
        elif "空头" in trend_type:
            base_op = "观望信号（价量尚可，但处于下跌均线，严控仓位）"
        else:
            base_op = "买入/持有信号（价量共振走强）,想想赚钱的感觉！"
    elif price_score >= 50 and volume_score < 50:
        base_op = "观望信号（价强量弱，无量上涨不宜加仓）"
    elif price_score < 50 and volume_score >= 50:
        base_op = "观望信号（量强价弱，反弹减仓）"
    else:
        base_op = "卖出/空仓信号（价量双弱）, 想想亏钱的日子！"

    # 拼接：基础操作 + 趋势纪律 + 风险提示
    full_op = f"{base_op}{turn_tip}"
    operation = f"{full_op}【{risk_notice}】" if risk_notice else full_op

    # ===================== 返回字典：兼容旧字段 + 新增反转拐点信息 =====================
    res_dict = {
        # 原版保留全部字段，业务无修改
        "最终综合评分": final_score,
        "最终仓位等级": base_level,
        "建议仓位区间": final_position,
        "操作建议": operation,
        "价格评分": price_score,
        "成交量评分": volume_score,
        "价格维度详情": price_result,
        "成交量维度详情": volume_result,

        # 扩展字段
        "当前趋势档位": trend_type,
        "趋势允许最大仓位": f"{max_allow_pos * 100:.0f}%",
        "是否单日放量": is_volume_spike,
        "动态价量权重": {"价格权重": w_price, "成交量权重": w_volume},
        "均线行情数据": {
            "现价": round(price_today, 2),
            "MA5价格": round(price_ma5, 2),
            "MA16价格": round(price_ma16, 2),
            "当日成交额": vol_today,
            "昨日成交额": vol_yest,
            "前日成交额": vol_day_before_yest,
            "5日均成交额": vol_ma5
        },
        # 新增反转拐点标记（连续3日条件）
        "拐点预警": {
            "多头转跌风险(连续3日缩量破5日线)": turn_bear_warn,
            "底部反转信号(连续3日放量站稳5日线)": turn_bull_signal
        }
    }

    print("价格分析结果：", price_result)
    print("成交量分析结果：", volume_result)
    return price_result, volume_result, res_dict


def calc_reasonable_position(total_amo):
    """
    优化仓位分布：结合今日成交额与各均值的比值，分段提升灵敏度
    :param total_amo: [今日成交额, 昨日成交额, 5日均值, 16日均值, 30日均值]
    :return: 仓位层数（int, 1~8）
    """

    price_result = volume_based_position_analysis(total_amo[5], total_amo[6], total_amo[7], total_amo[8])
    print(price_result)
    volume_result = volume_based_position_analysis(total_amo[0], total_amo[1], total_amo[2], total_amo[3])
    print(volume_result)

    # 取出两个维度的综合评分
    price_score = price_result["综合评分"]
    volume_score = volume_result["综合评分"]

    # ======================
    # 最终综合评分（价格40% + 量能60%，最科学的权重）
    # ======================
    final_score = round(price_score * 0.4 + volume_score * 0.6, 1)

    # ======================
    # 最终仓位等级
    # ======================
    if final_score >= 90:
        final_level = "重仓"
        final_position = "80%~100%"
    elif final_score >= 70:
        final_level = "中高仓"
        final_position = "60%~80%"
    elif final_score >= 50:
        final_level = "中等仓"
        final_position = "40%~60%"
    elif final_score >= 30:
        final_level = "轻仓"
        final_position = "20%~40%"
    else:
        final_level = "空仓/观望"
        final_position = "0%~20%"

    # ======================
    # 操作信号（双维度共振判断）
    # ======================
    if price_score >= 50 and volume_score >= 50:
        operation = "买入/持有信号（价量共振走强）,想想赚钱的感觉！"
    elif price_score >= 50 and volume_score < 50:
        operation = "观望信号（价强量弱，谨慎）"
    elif price_score < 50 and volume_score >= 50:
        operation = "观望信号（量强价弱，反弹减仓）"
    else:
        operation = "卖出/空仓信号（价量双弱）, 想想亏钱的日子！"

    # ======================
    # 最终返回结果
    # ======================
    return price_result, volume_result, {
        "最终综合评分": final_score,
        "最终仓位等级": final_level,
        "建议仓位区间": final_position,
        "操作建议": operation,
        "价格评分": price_score,
        "成交量评分": volume_score,
        "价格维度详情": price_result,
        "成交量维度详情": volume_result
    }


def volume_based_position_analysis(today_volume, yesterday_volume, ma5, ma16):
    # 数据校验（已删除 ma30）
    if any(not isinstance(v, (int, float)) or v <= 0 for v in [today_volume, yesterday_volume, ma5, ma16]):
        return {"error": "所有输入必须为大于0的数字"}

    # ---------------------
    # 1. 短期动能评分（不变）
    # ---------------------
    day_growth = (today_volume - yesterday_volume) / yesterday_volume
    vs_ma5_ratio = today_volume / ma5
    short_score = 50 + (day_growth * 150) + ((vs_ma5_ratio - 1) * 120)
    short_score = max(0, min(100, short_score))

    # ---------------------
    # 2. 中期趋势评分（已删除 ma30）
    # ---------------------
    ma_trend = 0
    if ma5 > ma16:
        ma_trend = 1
    elif ma5 < ma16:
        ma_trend = -1

    # 原基于ma30 → 替换为 ma16（最合理等价替换）
    vol_strength = max(-30, min(30, (today_volume / ma16 - 1) * 100))
    mid_score = 50 + (ma_trend * 25) + vol_strength
    mid_score = max(0, min(100, mid_score))

    # ---------------------
    # 3. 市场热度评分（已删除 ma30）
    # ---------------------
    health_ratio = ma5 / ma16
    heat_score = 50 + ((health_ratio - 1) * 80) + ((today_volume / ma16 - 1) * 40)
    heat_score = max(0, min(100, heat_score))

    # ---------------------
    # 4. 综合评分（不变）
    # ---------------------
    total = short_score * 0.40 + mid_score * 0.35 + heat_score * 0.25
    total = round(total, 2)

    # ---------------------
    # 5. 仓位建议（不变）
    # ---------------------
    if total >= 80:
        level = "重仓"
        pos = 80 + (total - 80) / 20 * 20
    elif total >= 60:
        level = "中高仓"
        pos = 60 + (total - 60) / 20 * 20
    elif total >= 40:
        level = "中等仓"
        pos = 40 + (total - 40) / 20 * 20
    elif total >= 20:
        level = "轻仓"
        pos = 20 + (total - 20) / 20 * 20
    else:
        level = "空仓"
        pos = total / 20 * 20

    pos = round(max(0, min(100, pos)), 1)

    # ---------------------
    # 返回结果（已删除 ma30 相关）
    # ---------------------
    return {
        "综合评分": total,
        "仓位等级": level,
        "建议仓位": f"{pos}%",
        "分项评分": {
            "短期动能": round(short_score, 1),
            "中期趋势": round(mid_score, 1),
            "市场热度": round(heat_score, 1),
        },
        "成交量状态": {
            "日环比": f"{day_growth:.1%}",
            "vs5日均": f"{vs_ma5_ratio - 1:.1%}",
            "均线排列": "多头" if ma_trend == 1 else "空头" if ma_trend == -1 else "震荡",
            "量能强度": f"{vol_strength:.1f}分"
        }
    }


def send_wechat_jrj(jrj):
    total_inflow = 0
    msg = str(jrj['td']) + " 大盘云图："
    for jr in jrj['hqs']:
        if float(jr['rval']) < 1000000000:
            continue
        total_inflow += float(jr['rval'])
        msg = msg + "\n #" + jr['name'] + \
              " - 净流入:" + str(round(float(jr['rval']) / 100000000, 2)) + "亿"
    total_inflow_亿 = round(total_inflow / 100000000, 2)
    msg = msg + "\n总净流入金额：" + str(total_inflow_亿) + "亿"
    wx.ChatWith(who)
    send_wechat(msg)


def send_wechat_stock(stop_list, select_list):
    # if len(stop_list) > 2:
    #     msg = "搞短线！！！ \n"
    #
    # if len(stop_list) < 3:
    #     msg = "弃短线！！！ \n"

    msg = todayStr + "涨停个股信息："
    for stop in stop_list:
        info = get_mysql(stop['code'])
        msg = msg + "\n " + " - " + stop['code'] + ' [ ' + str(stop['times']) + ' / ' + str(
            stop['limit_times']) + ' ] : #' + \
              stop['name'] + "\n " + ", ".join(str(x) for x in stop['totalInd'])
        if info is not None:
            msg = msg + "\n " + info[4]
    send_wechat(msg)

    if len(select_list) == 0:
        return

    select_list_sorted = sorted(select_list, key=lambda x: (x['amo_times'] + x['times'] + x['limit_times']),
                                reverse=True)[:25]
    select_list_sorted = sorted(select_list_sorted, key=lambda x: (x['MA4-0'][1] / x['MA16-0'][1]), reverse=True)
    msg2 = todayStr + "趋势个股信息："
    for select in select_list_sorted[:15]:
        info = get_mysql(select['code'])
        msg2 = msg2 + "\n " + str(select['times']) + " -> " + select['code'] + ' : #' + select[
            'name'] + "\n " + ", ".join(str(x) for x in select['indicator'])
        if info is not None:
            msg2 = msg2 + "\n " + info[2] + "\n " + info[4]
    send_wechat(msg2)


def send_wechat_bk(select_list):
    if len(select_list) == 0:
        return
    wx.ChatWith(who)
    msg = todayStr + "板块信息："
    for stop in select_list:
        msg = msg + "\n " + stop['code'] + ':#' + stop['name'] + " ->" + str(stop['ahs'])
    send_wechat(msg)
    print("发送结束！")


def send_wechat_ind(select_list, title):
    if len(select_list) == 0:
        return
    wx.ChatWith(who)
    msg = todayStr + " " + title
    i = 0
    for stop in select_list:
        msg = msg + "\n" + stop['industry'] + " ->" + str(stop['stop_times']) \
              + "\n  #" + ',#'.join([item for item in stop['stop_details']])
        i += 1
        if stop['stop_times'] < 4:
            break
        if i >= 8:
            break
        # if i < 5 and i % 8 == 0:
        #     send_wechat(msg)
        #     msg = todayStr + " " + title

    send_wechat(msg)
    print(title + "发送结束！")


def send_wechat_rank(select):
    if len(select) == 0:
        return
    wx.ChatWith(who)
    msg = todayStr + " 今日涨停榜"
    i = 0
    for stop in select[:10]:
        if stop['times'] < 3:
            break
        msg = msg + "\n#" + stop['name'] + " -> " + str(stop['times']) + "\n || " + stop['industry']
        # + "\n || " + '*'.join([item for item in stop['concept']])
        i += 1
        # if i < 5 and i % 9 == 0:
        #     send_wechat(msg)
        #     msg = todayStr + " 今日涨停榜"

    send_wechat(msg)
    print("发送结束！")

# stock = {
#     'code': row[0],
#     'name': row[1],
#     'industry': row[2],
#     'address': row[3],
#     'times': row[5],
#     'concept': row[4].split(',')
# }
# stock_list = []
# ak = {
#     'code': 'sh600187',
#     'name': '国中水务',
#     'times': 8
# }
# stock_list.append(ak)
# send_wechat_stock(stock_list, None)
