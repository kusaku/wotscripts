# Embedded file name: scripts/client/adapters/ITutorialLesson.py
from Helpers.i18n import localizeTutorial
from adapters.DefaultAdapter import DefaultAdapter
import _tutorial_data

class ITutorialLessonClientAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOb = super(ITutorialLessonClientAdapter, self).__call__(account, ob, **kw)
        lessonID = kw['idTypeList'][0][0]
        adaptedOb['lessonNumber'] = _tutorial_data.TutorialData.lesson[lessonID].id + 1
        adaptedOb['lessonName'] = localizeTutorial(_tutorial_data.TutorialData.lesson[lessonID].lobbyTitle)
        adaptedOb['disabledTitle'] = localizeTutorial(_tutorial_data.TutorialData.lesson[lessonID].disabledTitle)
        adaptedOb['rewardExp'] = _tutorial_data.TutorialData.lesson[lessonID].countExperience
        adaptedOb['rewardCreds'] = _tutorial_data.TutorialData.lesson[lessonID].countCredits
        adaptedOb['rewardGold'] = _tutorial_data.TutorialData.lesson[lessonID].countGold
        return adaptedOb


class ITutorialLessonListAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOb = super(ITutorialLessonListAdapter, self).__call__(account, ob, **kw)
        adaptedOb['lessons'] = [ lesson.id for lesson in _tutorial_data.TutorialData.lesson ]
        return adaptedOb


class ITutorialPromptParamsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOb = super(ITutorialPromptParamsAdapter, self).__call__(account, ob, **kw)
        lessonID = kw['idTypeList'][0][0]
        lessonData = _tutorial_data.TutorialData.lesson[lessonID]
        adaptedOb['isBonus'] = True
        adaptedOb['nameReward'] = localizeTutorial(lessonData.nameReward)
        adaptedOb['countCredits'] = lessonData.countCredits
        adaptedOb['nameCredits'] = localizeTutorial(lessonData.nameCredits)
        adaptedOb['countExperience'] = lessonData.countExperience
        adaptedOb['nameExperience'] = localizeTutorial(lessonData.nameExperience)
        adaptedOb['countGolds'] = lessonData.countGold
        adaptedOb['nameGolds'] = localizeTutorial(lessonData.nameGold)
        adaptedOb['title'] = localizeTutorial(lessonData.lobbyTitle)
        adaptedOb['titleCompleted'] = localizeTutorial(lessonData.lobbyTitleCompleted)
        adaptedOb['description1'] = localizeTutorial(lessonData.lobbyDescription1)
        adaptedOb['description2'] = localizeTutorial(lessonData.lobbyDescription2)
        adaptedOb['type'] = 1
        adaptedOb['lessonIndex'] = lessonID
        adaptedOb['isLastLesson'] = lessonID >= len(_tutorial_data.TutorialData.lesson) - 1
        return adaptedOb