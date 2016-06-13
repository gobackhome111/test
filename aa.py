#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import os
import sys

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

define("port", default=5000, help="run on this port", type=int)
define("debug", default=False, help="enable debug mode")
define("cache", default=True, help="enable memcached mode")
define("project_path", default=sys.path[0], help="deploy_path")

tornado.options.parse_command_line()

URLS = (
    (r'box\.90iktv\.com',
        (r"/qrcode/?", 'handler.box.QrdataHandler'),
        (r"/deviceid/?", 'handler.box.DeviceIdHandler'),
        (r"/getuserinfo/?",'handler.userapi.UserInfoHandler'),
        (r"/getcurmeal/?","handler.userapi.UserMealHandler"),
        (r"/getmealinfo/?","handler.userapi.MealInfoHandler"),
        (r"/deluserinfo/?",'handler.userapi.DelUserInfoHandler'),
        (r'/getcardlist/?','handler.userapi.CardListHandler'),
        (r'/getcardinfo/?','handler.userapi.CardInfoHandler'),
        #(r'/delusermeal/?','handler.userapi.DelUserMealHandler'),
        (r'/usecardinfo/?','handler.userapi.CardTradeHandler'),
        (r'/searchusermeal/?','handler.userapi.SearchUserMealHandler'),
        (r'/searchtradeinfo/?','handler.userapi.SearchTradeInfoHandler'),
        (r'/searchdownloadno/?','handler.userapi.SearchDownloadNoHandler'),
        (r'/changeusermeal/?','handler.userapi.ChangeUserMealHandler'),
        (r'/changeuserdevice/?','handler.userapi.ChangeUserDeviceHandler'),
        (r'/registuser/?','handler.userapi.RegistUserHandler'),
        (r'/mikiuser/?','handler.userapi.MikiDeviceHandler'),
        (r'/checknumbers/?','handler.userapi.CheckNumbersHandler'),
        (r'/userland/?','handler.userapi.UserLandHandler'),
        (r'/sessionland/?','handler.userapi.SessionLandHandler'),
        (r'/uploadrecords/?','handler.userapi.UploadRecordsHandler'),
        (r'/getrecords/?','handler.userapi.GetRecordsHandler'),
        (r'/uploadcollection/?','handler.userapi.UpCollectHandler'),
        (r'/getcollection/?','handler.userapi.GetCollectHandler'),
        (r'/getmikicollection/?','handler.userapi.GetCollectForMikiHandler'),
        (r'/searchmikicollection/?','handler.userapi.SearchCollectForMikiHandler'),
        (r'/getcityname/?','handler.userapi.GetCityNameHandler'),
        (r'/getcityweather/?','handler.userapi.GetCityWeatherHandler'),
        (r'/getpushedmsg/?','handler.userapi.GetPushMsgHandler'),
        (r'/dealpushedmsg/?','handler.userapi.DealPushMsgHandler')
    ),
    (r'api\.90iktv\.com',
        (r"/musicinfo/?", 'handler.api.MusicInfoHandler'),
        (r"/getmvurl/?", 'handler.api.MVUrlHandler'),
        (r"/getfileurl/?", 'handler.api.FileUrlHandler'),
        (r"/regetfileurl/?", 'handler.api.ReFileUrlHandler'),
        (r"/vodrec/?",     'handler.api.VodRecordHandler'),
        (r"/getvodrec/?",  'handler.api.GetVodRecordHandler'),
        (r"/score/?",      'handler.api.ScoreHandler'),
        (r'/upload/?', 'handler.api.UploadHandler'),
        (r"/adddowninfo/?","handler.userapi.DownLoadLogHandler"),
        (r"/gettradestatus/?","handler.userapi.TradeInfoHandler"),
        #(r"/getnewfileurl/?","handler.userapi.FileUrlHandler"),
        (r"/getnewfileurl/?","handler.userapi.FileUrlLimitHandler"),
        (r"/gettradeqrcode/?","handler.userapi.AlipayqrcodeHanlder"),
        (r"/alipaycallback/?","handler.userapi.AlipayCallHandler"),
        (r"/alipaycallbackfortheme/?","handler.userapi.AlipayCallForThemeHandler"),
        (r"/alipaycallbackforthemesingle/?","handler.userapi.AlipayCallForThemeSingleHandler"),
        (r"/gettradeqrcodetheme/?","handler.userapi.AlipayqrcodeForThemeHandler"),
        (r"/gettradeqrcodethemepackage/?","handler.userapi.AlipayqrcodeForThemePackageHandler"),
        (r"/canceltrade/?","handler.userapi.CancelTradeHandler"),
        (r'/getrankinfo/?','handler.api.GetRankInfoHandler'),
        (r'/getmusicrank/?','handler.api.GetMusicRankHandler'),
        (r"/getmovieinfo/?","handler.api.MovieInfoHandler"),
        (r"/getmoviefile/?","handler.api.MovieUrlHandler"),
        (r"/getuploadkey/?","handler.api.GetUploadKeyHandler"),
        (r"/alipaycallbackformovie/?","handler.userapi.AlipayCallForMovieHandler"),
        (r"/gettradeqrcodemv/?","handler.userapi.AlipayqrcodeForMovieHandler"),
        (r"/cancelmovietrade/?","handler.userapi.CancelMovieTradeHandler"),
        (r"/getnewmovieinfo/?","handler.api.MovieInfo2Handler"),
        (r"/getnewmoviefile/?","handler.api.MovieUrl2Handler"),
        (r"/getusermovie/?","handler.api.UserMovieHandler"),
        (r"/getmovietradeinfo/?","handler.userapi.GetMoviesReportFormsHandler"),
        (r"/getmovielistinfo/?","handler.userapi.GetMovieListHandler"),
        (r"/ks3getfileurl/?","handler.api.JinshanFileUrlHandler"),
        (r"/getplusfileurl/?","handler.userapi.FileUrlPlusHandler"),
        (r"/getroomcontrollerinfo/?","handler.userapi.RoomControllerInfoHandler"),
        (r"/getuserroomcontroller/?","handler.userapi.UserRoomControllerHandler"),
        (r"/alipaycallbackforroomcontroller/?","handler.userapi.AlipayCallForRoomControllerHandler"),
        (r"/gettradeqrcoderoomcontroller/?","handler.userapi.AlipayqrcodeForRoomControllerHandler"),
        (r"/getthemeinfo/?","handler.userapi.ThemeInfoHandler"),
        (r"/getthemepackageinfo/?","handler.userapi.ThemePackageInfoHandler"),
        (r"/getusertheme/?","handler.userapi.UserThemeHandler"),
        (r"/getlandinfo/?","handler.userapi.GetLandInfoHandler"),
        (r"/suggestin/?","handler.api.SuggestionHandler"),
        (r"/feedback/?","handler.api.ReciveSuggestHandler"),
        (r"/movieinfocontrol/?","handler.api.MovieInfoControlHandler"),
        (r"/moviedatacontrol/?","handler.api.MovieDataControlHandler"),
        (r"/usermealcontrol/?","handler.userapi.MealSearchControlHandler"),
        (r"/addmealcontrol/?","handler.userapi.MealAddControlHandler"),
        (r"/getareaboxinfo/?","handler.userapi.GetMacAreaInfoHandler"),
        (r"/getusersuggestion/?","handler.api.GetSugguestUserInfoHandler"),
        (r"/getsongsuggestion/?","handler.api.GetSugguestSongInfoHandler"),
        (r"/getproducttypeamount/?","handler.userapi.GetProductTypeAmount"),
        (r"/getproductversiondetail/?","handler.userapi.GetProductVersionDetailInfo"),
        (r"/getadvertisementpercent/?","handler.userapi.GetAdvertisementPercentHandler"),
        (r"/productactivity/?", 'handler.box.ProductActivityHandler'),
        (r"/getdownloadinfo/?","handler.userapi.GetDownloadInfoHandler"),
    ),
    (r'wx\..*90iktv\.com',
        (r"/?", 'handler.wechat.IndexHandler'),
        (r"/rank/?", 'handler.wechat.RankHandler'),
        (r"/wechat/?", 'handler.wechat.WechatHandler'),
        (r"/fav/?", 'handler.wechat.FavHandler'),
        (r"/getqrcodes/?","handler.wechat.GetWxQtcodesHandler"),
        (r"/getvipsongs/?","handler.wechat.GetVipSongsHandler"),
        (r"/getnewmovieinfoweixin/?","handler.wechat.MovieInfoWeixinHandler"),
        (r'/getrankinfoweixin/?','handler.wechat.GetRankInfoWeixinHandler'),
    ),
)

class Application(tornado.web.Application):

    def __init__(self):
        settings = {
            "debug": options.debug,
            "gzip": True,
            "autoescape": None,
            "xsrf_cookies": False,
            "template_path": os.path.join(options.project_path, "tpl"),
            "static_path": os.path.join(options.project_path, "static"),
            "cookie_secret": "exoOr1WYSg6+W7lbDbmtNmt6U0ZmrkwbvnnqyWksvCY="
        }
        print settings
        tornado.web.Application.__init__(self, **settings)

        for spec in URLS:
            host = spec[0]
            patterns = spec[1:]
            if not options.debug:
                pass
            elif host.startswith('.*'):
                host = '.*$'
            else:
                subdomain, _, _ = host.partition(r'\.')
                _patterns = []
                for item in patterns:
                    _item = list(item)
                    _item[0] = '/%s%s' % (subdomain, _item[0])
                    _patterns.append(_item)
                patterns = _patterns
                host = '.*$'
            self.add_handlers(host, patterns)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    t
