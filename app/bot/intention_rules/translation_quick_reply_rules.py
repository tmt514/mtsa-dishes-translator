from app.bot.rule import Rule, ForceChangeStateException, transition
from app.models import db, Term, Photo, Location

STATE_ENGLISH_TO_CHINESE_OK = 'STATE_ENGLISH_TO_CHINESE_OK'
STATE_ENGLISH_TO_CHINESE_QR = 'STATE_ENGLISH_TO_CHINESE_QR'
STATE_CHINESE_TO_ENGLISH_OK = 'STATE_CHINESE_TO_ENGLISH_OK'
STATE_CHINESE_TO_ENGLISH_QR = 'STATE_CHINESE_TO_ENGLISH_QR'



def handle_qr_adjustment(bot, user, msg, **template_params):
    """ 根據這個查詢的 term 是什麼東西，而做出正確的回應 """
    e = user.get_english()
    c = user.get_chinese()
    tr = msg['translated_string']
    term = Term.query.filter_by(english=e, chinese=c).first()
    qr = []

    if term == None:
        bot.bot_send_message(user.id, bot.reply_gen.translated_string(tr))
        return

    #########################################################
    ### Pokemon
    #########################################################
    categories = term.categories.all()
    for category in categories:
        if category.name == 'pokemon':
            qr.append(bot.reply_gen.make_quick_reply(
                title='圖鑑',
                payload="PAYLOAD_POKEMON_INFO:%s"%e,
                image_url="http://emojis.slackmojis.com/emojis/images/1450464069/186/pokeball.png?1450464069"))




    #########################################################
    ### Category
    #########################################################
    # 檢查這個 Term 是不是個 Location
    # 以後資料齊全以後可以把這個刪掉，或改為 offline

    # 如果有 category, 那麼可以取得更多資訊
    if term.categories.count() > 0:
        qr.append(bot.reply_gen.QUICK_REPLY_MORE)
    

    # 如果所有都不符合，就回到預設吧
    if len(qr) == 0:
        qr = None

    # 送出訊息(決定要不要帶圖片、或是純文字訊息等等)
    bot.bot_send_message(user.id, bot.reply_gen.translated_string(tr, quick_replies=qr))
    # 如果是神奇寶貝 才要放圖片?
    # if q is not None and q.photos.first() is not None:
    #    bot.bot_send_message(user.id, bot.reply_gen.image(q.photos.first().url))



class TranslationQRRules(Rule):

    @transition(STATE_ENGLISH_TO_CHINESE_QR, {'text':''}, STATE_ENGLISH_TO_CHINESE_OK)
    def english_to_chinese_qr_adjustment(self, bot, user, msg, **template_params):
        handle_qr_adjustment(bot, user, msg, **template_params)
        return True

    @transition(STATE_CHINESE_TO_ENGLISH_QR, {'text':''}, STATE_CHINESE_TO_ENGLISH_OK)
    def chinese_to_english_qr_adjustment(self, bot, user, msg, **template_params):
        handle_qr_adjustment(bot, user, msg, **template_params)
        return True

