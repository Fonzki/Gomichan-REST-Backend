import json
from gtts import gTTS

from flask_restful import Resource, Api, reqparse
from models.line import LineModel
from models.phoneme import PhonemeModel, PhonemeInstanceModel
from models.syllable import SyllableModel, SyllableInstanceModel
from models.word import WordModel, WordInstanceModel
from models.phrase import PhraseModel
from models.role_phrase import RolePhraseModel

class LineBuilder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('json', required=True, help="need json")

    def pnames_to_instances(self, pnames):
        instance_ids = []
        for p in pnames:
            phoneme = PhonemeModel.find_by_name(p['name'])
            instance = PhonemeInstanceModel(phoneme.id)
            instance.save_to_db()
            instance_ids.append(instance.json()['id'])
        return instance_ids

    def make_syllable_instance(self, s_id):
        instance = SyllableInstanceModel(s_id)
        instance.save_to_db()
        return instance.id

    def make_TTS_file(self, text, filename):
        language = 'en'
        sound_file = gTTS(text=text, lang=language, slow=False)
        sound_file.save(filename)

    def make_syllable(self, spelling, sound_link, filename, pids):
        model = SyllableModel.find_by_spelling(spelling)
        if not model:
            model = SyllableModel(spelling, sound_link, pids)
            self.make_TTS_file(spelling, filename)
            print("sound: "+sound_link)
            model.save_to_db()

        return self.make_syllable_instance(model.id)

    def make_word_instance(self, w_id, display):
        instance = WordInstanceModel(w_id, display)
        instance.save_to_db()
        return instance

    def make_word_from_syllable(self, spelling, display, sound_link, stress, sids):
        #check for model 
        model = WordModel.find_by_spelling(spelling)
        if not model:
            model = WordModel(spelling, display, sound_link, sids, stress)

            # only run for multi-syllable words
            # single syllable words have no stress( -1 index)
            if stress > -1:
                self.make_TTS_file(spelling, spelling+'.mp3')

            model.save_to_db()

        #create instance 
        return self.make_word_instance(model.id, display)

    def make_syllable_filename(self, phonemes):
        filename = ""

        for p in phonemes:
            filename += p['name']

        filename += ".mp3"
        return filename

    def make_word_list_syllables(self, word_list):
        mids = []
        wids = []
        for word in word_list:
            if word['repeat'] > -1:
                word_id = mids[word['repeat']]
                instance = WordInstanceModel(word_id, word['display'])
                instance.save_to_db()
                wids.append(instance.id)
                mids.append(word_id)
                continue

            if not word['defined']:
                sids = []
                for syllable in word['syllables_to_get']:
                    spelling = syllable['name']
                    sound_link = syllable['sound_link']
                    pids = self.pnames_to_instances(syllable['phonemes'])
                    filename = self.make_syllable_filename(syllable['phonemes'])
                    sids.append(self.make_syllable(spelling, sound_link, filename, pids))

                spelling = word['spelling']
                display = word['display']
                sound_link = word['sound_link']
                stress = word['stress']
                word_instance = self.make_word_from_syllable(spelling, display, sound_link, stress, sids)
                wids.append(word_instance.id)
                mids.append(word_instance.word_id)

            else:
                word_id = word['id']
                instance = WordInstanceModel(word_id, word['display'])
                instance.save_to_db()
                wids.append(instance.id)
                mids.append(word_id)

        return wids

    def make_filename_from_wids(self, wids):
        filename = ""
        for wid in wids:
            instance = WordInstanceModel.find_by_id(wid)
            word = WordModel.find_by_id(instance.word_id)

            filename += word.spelling + "-"

        filename = filename[:-1] + ".mp3"
        return filename
    
    def make_text_from_wids(self, wids):
        text = ""
        for wid in wids:
            instance = WordInstanceModel.find_by_id(wid)
            word = WordModel.find_by_id(instance.word_id)
            text += word.spelling + " "

        text = text[:-1]
        return text

    def make_roles_from_raw(self, phrase_list, word_ids):
        wid_index = 0
        role_pids = []
        for phrase in phrase_list:
            sub_wids = word_ids[wid_index:wid_index+phrase['word_count']]
            wid_index += phrase['word_count']

            display = phrase['display']
            sound_link = phrase['sound_link']
            
            # only make TTS for multi-word phrases
            if '-' in sound_link:
                filename = self.make_filename_from_wids(sub_wids)
                text = self.make_text_from_wids(sub_wids)
                self.make_TTS_file(text, filename)
            instance = PhraseModel(sub_wids, display, sound_link)
            instance.save_to_db()
            role_instance = RolePhraseModel(
                instance.id, 
                phrase['role'], 
                phrase['translation'],
                phrase['punctuation']
            )
            role_instance.save_to_db()

            role_pids.append(role_instance.id)
        
        return role_pids

    def post(self):
        data = LineBuilder.parser.parse_args()
        raw = json.loads(data['json'])
        
        word_ids = self.make_word_list_syllables(raw['word_list'])
        role_pids = self.make_roles_from_raw(raw['phrase_list'], word_ids)

        translation = raw['translation']
        start = raw['start']
        duration = raw['duration']
        video_link = raw['video_id']

        line_instance = LineModel(translation, role_pids, video_link, start, duration)
        line_instance.save_to_db()
        
        return {'line': line_instance.json()}, 200
        #return {'message': 'its fucked mate'}, 500
