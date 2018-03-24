"""SUSTechAPP_Market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import Market.views as Marketviews
import Webfunc.views as Webfuncviews
import Management.views as Managementviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/registe/', Marketviews.registe),
    url(r'^user/login/', Marketviews.login),
    url(r'^user/test/', Marketviews.test),
    url(r'^user/isPhoneRegisted/', Marketviews.isPhoneRegisted),
    url(r'^user/saveInfo/', Marketviews.saveInfo),
    url(r'^user/getInfo/', Marketviews.getInfo),
    url(r'^user/uploadheadimage/', Marketviews.uploadheadimage),
    url(r'^user/getUserDetail/', Marketviews.getUserDetail),
    url(r'^user/getUserQQ/', Marketviews.getUserQQ),
    url(r'^user/getDealed/', Marketviews.getDealed),
    url(r'^user/getDealing/', Marketviews.getDealing),
    url(r'^user/sell_deal/', Marketviews.sell_deal),
    url(r'^user/changepwd/', Marketviews.changepwd),
    
    # url(r'^user/getPushID/', Marketviews.getPushID),

    url(r'^user/activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$',
        Marketviews.active_user),

    url(r'^menu/pubsell/', Marketviews.sell_pub),
    url(r'^menu/getsell/', Marketviews.sell_get),


    url(r'^info/getDeltaDateForCT/', Marketviews.getDeltaDateForCT),
    url(r'^info/getComment/', Marketviews.getComment),
    url(r'^info/doComment/', Marketviews.doComment),

    url(r'^blamewall/getWhoStarBlameWall/', Marketviews.getWhoStarBlameWall),
    url(r'^blamewall/starBlameWall/', Marketviews.starBlameWall),
    url(r'^blamewall/unstarBlameWall/', Marketviews.unstarBlameWall),
    url(r'^blamewall/getBlameWallInfo/', Marketviews.getBlameWallInfo),
    url(r'^info/getLimitedBlameWallInfo/', Marketviews.getLimitedBlameWallInfo),

    url(r'^info/getUserNumberInfo/', Marketviews.getUserNumberInfo),
    url(r'^info/getBusTime/', Marketviews.getBusTime),
    url(r'^info/getEasyBusInfo/', Marketviews.getEasyBusInfo),
    url(r'^info/getlocation/', Marketviews.getlocation),
    url(r'^info/putlocation/', Marketviews.putlocation),
    url(r'^info/getSustcMainNews/', Marketviews.getSustcMainNews),
    url(r'^info/getSustcForumInfo/', Marketviews.getSustcForumInfo),
    url(r'^info/getGPAinfo/', Marketviews.getGPAinfo),
    url(r'^info/getTeacherInfo/', Marketviews.getTeacherInfo),
    url(r'^info/SearchBooks/', Marketviews.SearchBooks),
    url(r'^info/getMainPagePicture/', Marketviews.getMainPagePicture),
    url(r'^info/getWeather/', Marketviews.getWeather),
    url(r'^info/isLibResigned/', Marketviews.isLibResigned),
    url(r'^info/LibResign/', Marketviews.LibResign),
    url(r'^info/getActivity/', Marketviews.getActivity),
    url(r'^info/getLimitedActivity/', Marketviews.getLimitedActivity),
    url(r'^info/getTeacherByID/', Marketviews.getTeacherByID),
    url(r'^info/getAllMyData/', Marketviews.getAllMyData),
    url(r'^info/getSellDetail/', Marketviews.getSellDetail),
    url(r'^info/jwxtResign/', Marketviews.jwxtResign),
    url(r'^info/getOtherActivity/', Marketviews.getOtherActivity),
    url(r'^info/getMainFunction/', Marketviews.getMainFunction),
    url(r'^info/getMainInfo/', Marketviews.getMainInfo),
    
    # url(r'^info/getClassTableByDate/', Marketviews.getClassTableByDate),
    url(r'^info/getClassTableAvailabeDate/',
        Marketviews.getClassTableAvailabeDate),
    url(r'^info/getClassTableByWeekday/', Marketviews.getClassTableByWeekday),
    url(r'^info/getClassdetail/', Marketviews.getClassdetail),
    url(r'^info/getGPAdetail/', Marketviews.getGPAdetail),
    url(r'^info/getNextClass/', Marketviews.getNextClass),
    url(r'^info/getAppMsg/', Marketviews.getAppMsg),

    url(r'^info/checkoutVersion/', Marketviews.checkoutVersion),
    url(r'^info/getWenjuan/', Marketviews.getWenjuan),

    url(r'^action/addForumToCalendar/', Marketviews.addForumToCalendar),
    url(r'^action/putWallContent/', Marketviews.putWallContent),
    url(r'^action/OneKeyBorrowBooks/', Marketviews.OneKeyBorrowBooks),
    url(r'^action/putPictureWords/', Marketviews.putPictureWords),
    url(r'^action/pubActivity/', Marketviews.pubActivity),
    url(r'^action/appointTeacher/', Marketviews.appointTeacher),
    url(r'^action/addActivityToCalendar/', Marketviews.addActivityToCalendar),
    url(r'^action/cancelActivity/', Marketviews.cancelActivity),
    url(r'^action/updateUserInfo/', Marketviews.updateUserInfo),


    url(r'^web/login/', Webfuncviews.login),
    url(r'^web/getClassNameList/', Webfuncviews._getClassNameList),
    url(r'^web/getClasstable/', Webfuncviews._getClasstable),
    url(r'^web/getClassLink/', Webfuncviews._GetClassLink),
    url(r'^web/getCheckPay/', Webfuncviews._getCheckPay),
    url(r'^web/getClassXKed/', Webfuncviews._getClassXKed),
    url(r'^web/app_getKey/', Webfuncviews.app_getKey),
    url(r'^web/setXKtime/', Webfuncviews.setXKtime),

    url(r'^management/getTotalNums/', Managementviews.getTotalNums),
    url(r'^management/SystemOperate/', Managementviews.SystemOperate),
    url(r'^management/searchUserInfo/', Managementviews.searchUserInfo),


]
