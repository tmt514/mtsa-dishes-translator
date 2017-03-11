from app.bot.rule import Rule, ForceChangeStateException, transition
from app.models import db, Term, Photo, Location
from app.bot.reply_generator import GenericTemplate


STATE_NEW = 'new'
PAYLOAD_LOCATION_INFO = 'PAYLOAD_LOCATION_INFO'

class LocationIntentionRules(Rule):

    @transition(STATE_NEW, {'quick_reply': {'payload': PAYLOAD_LOCATION_INFO}}, STATE_NEW)
    def rule_location_info(self, bot, user, msg, **template_params):
        location_id = int(msg['quick_reply'].get('target'))
        location = Location.query.get(location_id)
        if location is None:
            return True

        term = Term.query.filter_by(english=location.name.lower().strip()).first()
        
        reply = GenericTemplate()
        photo = location.photos.first()
        image_url = None
        if photo is not None:
            image_url = photo.url
        sub = None
        if term is not None:
            sub = term.chinese
        
        reply.add_element(title=location.name, subtitle=sub, default_action={"type":"web_url", "url":location.yelp_url}, image_url=image_url)
        reply = reply.generate()

        # reply['quick_replies'] = bot.reply_gen.add_quick_replies()
        bot.bot_send_message(user.id, reply)
        return True
