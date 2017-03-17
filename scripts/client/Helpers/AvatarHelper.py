# Embedded file name: scripts/client/Helpers/AvatarHelper.py


def getAvatarSkillsList(avatarEntity):
    if len(avatarEntity.crewSkills) == 0:
        return []
    return map(lambda e: e['key'], avatarEntity.crewSkills[0]['skills'])