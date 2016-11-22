import glob
import json
import os
import re
from collections import OrderedDict

import nltk

from ne import EN

whitelist = {
    "Brotherhood without Banners",
    "Cripples , Bastards and Broken Things",
    "Fire and Blood",
    "Battle at the Mummer's Ford",
    "An History of Aegon the Conqueror and His Conquest of Westeros",
    "Davos",
    "What is Dead May Never Die",
    "You Win or You Die",
    "We Do Not Sow",
    "Razdal mo Eraz",
    "Prendahl na Ghezn",
    "Yezzan zo Qaggaz"
    "Gilly",
    "Winter is Coming",
    "House of Black and White",
    "The Mountain and the Viper",
    "Valar morghulis",
    "Unbowed , Unbent , Unbroken",
    "Thin man",
    "The Watchers on the Wall",
    "The Wars to Come",
    "The Tickler",
    "The Lion and the Rose",
    "Regent and Protector of the Realm",
    "Children of the Forest",
    "A Man Without Honor",
    "The Bear and the Maiden Fair",
    "Maester Aemon",
    "Sam",
    "Hizdahr zo Loraq",
    "The Wolf and the Lion",
    "Kraznys",
    "The Unsullied",
    "Kraznys mo Nakloz",
    "Kissed by Fire",
    "Iron throne",
    "Jon",
    "And Now His Watch is Ended",
    "Mountain That Rides",
    "The Stallion That Mounts The World",
    "Growing Strong",
    "Two Swords",
    "The Prince That Was Promised",
    "Knight of the Flowers",
    "King in the North",
    "Lord Roose Bolton of the Dreadfort",
    "Lord Blackmont",
    "High Priestess of the Red Temple of Volantis",
    "Dornish Lords",
    "Princess Shireen of House Baratheon",
    "House of Black & White"
}

blacklisted_entities = {
    "King",
    "The King",
    "Aerys the Lannisters",
    "Castle Black of the White Walker",
    "Davos An History of Aegon the Conqueror",
    "During the Khalar",
    "Little Sam",
    "Meryn Trant Ser Meryn Trant",
    "Mud Gate",
    "Mummer 's Ford",
    "My Lord",
    "North Robb Stark",
    "Qyburn Grand Maester",
    "Sansa Meanwhile",
    "Sansa Robb",
    "Sansa the Moon Door",
    "Shireen 's Greyscale",
    "Stark Valyrian",
    "Stark of Winterfell",
    "Trystane Martell Jaime",
    "Your Grace",
    "Arya / Lanna",
    "Arya/Lanna",
    "Lannister - Tyrell",
    "Lannister / Tyrell",
    "Brother",
    "Boy",
    "Black Rat",
    "Battle",
    "Davos History of Aegon the Conqueror",
    "Dead May Never Die",
    "Die",
    "Direwolves",
    "Do Sow",
    "Eraz",
    "Fuck",
    "Gilly the Dragonglass",
    "Heart",
    "First",
    "Yezzan",
    "X-shaped",
    "Winter",
    "Win",
    "White",
    "Viper",
    "Valar",
    "Unbent",
    "Unbowed",
    "Unbroken",
    "Thin",
    "The Watchers",
    "The Wars",
    "The Tickler–sadistically",
    "The",
    "Rose",
    "Regent",
    "Ran",
    "Other",
    "Others",
    "Other Children of the Forest",
    "Spies",
    "Soldiers",
    "Man Without Honor",
    "Maiden Fair",
    "Maester Aemon Sam",
    "Mad",
    "Loraq",
    "Lion",
    "Lannister/Tyrell",
    "Lannister-Tyrell",
    "Ladies",
    "Kraznys The Unsullied",
    "Kissed",
    "Iron",
    "Inn",
    "Houses Jon",
    "Horses",
    "Hold",
    "Hizdahr",
    "His Watch",
    "His Conquest of Westeros",
    "His",
    "Do",
    "Sow",
    "War",
    "History of Aegon the Conqueror",
    "Mountain",
    "Rides",
    "Mounts The World",
    "The Stallion",
    "Strong",
    "Swords",
    "The Prince",
    "Was Promised",
    "Flowers",
    "Fire",
    "Blood",
    "Burn",
    "Coming",
    "Cripples",
    "Bastards",
    "Broken Things",
    "Ravens",
    "Stick",
    "House of Black"
}

blacklisted_words = {
    "In",
    "To",
    "Now",
    "Suddenly",
    "However",
    "While",
    "He",
    "Reluctantly",
    "Stunned",
    "As",
    "At",
    "Far",
    "With",
    "Forced",
    "For",
    "Later",
    "Unable",
    "Some",
    "It",
    "A",
    "She",
    "Though",
    "After",
    "They",
    "When",
    "Also",
    "Both",
    "Crying",
    "Hearing",
    "Her",
    "If",
    "Ignoring",
    "Infuriated",
    "Making",
    "New",
    "Once",
    "One",
    "Pretending",
    "There",
    "AND",
    "Aboard",
    "Accompanied",
    "According",
    "Addressing",
    "Afterward",
    "Afterwards",
    "Again",
    "Against",
    "All",
    "Almost",
    "Alone",
    "Although",
    "Amidst",
    "An",
    "And",
    "Angered",
    "Annoyed",
    "Another",
    "Anyone",
    "Apart",
    "Arriving",
    "Ask",
    "Asking",
    "Assigning",
    "Atop",
    "Attacking",
    "Attended",
    "Aunt",
    "Aware",
    "Awoken",
    "B",
    "Back",
    "Because",
    "Before",
    "Bodies",
    "But",
    "By",
    "Circumstances",
    "Confused",
    "Confusion",
    "Considering",
    "Consoling",
    "Consulting",
    "Contemplating",
    "Convinced",
    "Convincing",
    "Correctly",
    "Cryptically",
    "Curious",
    "Deciding",
    "Deducing",
    "Delighted",
    "Denouncing",
    "Desperately",
    "Despite",
    "Discouraged",
    "Disgusted",
    "Dismissive",
    "Displaying",
    "Displeased",
    "Distraught",
    "Due",
    "During",
    "E",
    "Each",
    "Easily",
    "Either",
    "Elsewhere",
    "En",
    "Ended",
    "Enraged",
    "Even",
    "Eventually",
    "Everyone",
    "Exhausted",
    "Fascinated",
    "Fearful",
    "Filled",
    "Finally",
    "Finding",
    "Fortunately",
    "From",
    "Frustrated",
    "Furthermore",
    "Given",
    "Having",
    "Here",
    "Hoping",
    "Horrified",
    "Hundreds",
    "I",
    "Immediately",
    "Impressed",
    "Increasingly",
    "Indeed",
    "Inevitably",
    "Inside",
    "Insisting",
    "Instead",
    "Intending",
    "Interrogating",
    "Intrigued",
    "Just",
    "Leave",
    "Leaving",
    "Let",
    "Like",
    "Looking",
    "M'Lord",
    "Meanwhile",
    "More",
    "Moreover",
    "Much",
    "Mutiny",
    "My",
    "Near",
    "Nearby",
    "Neither",
    "Nevertheless",
    "News",
    "No",
    "None",
    "Nonetheless",
    "Nor",
    "Not",
    "Nothing",
    "Noticing",
    "Numerous",
    "O",
    "Obedient",
    "Oblivious",
    "Of",
    "Oh",
    "On",
    "Only",
    "Ordered",
    "Out",
    "Outside",
    "Over",
    "Present - day",
    "Prior",
    "Privately",
    "Prologue",
    "Quickly",
    "Raising",
    "Rather",
    "Realizing",
    "Recalling",
    "Recognizing",
    "Refusing",
    "Released",
    "Reminding",
    "Reporting",
    "Resignedly",
    "Restraining",
    "Returning",
    "Reuniting",
    "Revealing",
    "Satisfied",
    "Several",
    "Severely",
    "Shortly",
    "Since",
    "So",
    "Someone",
    "Somewhat",
    "Somewhere",
    "Soon",
    "Still",
    "Stopping",
    "Subsequently",
    "Such",
    "Summoning",
    "Surprisingly",
    "That",
    "Their",
    "Therefore",
    "These",
    "This",
    "Those",
    "Through",
    "Thus",
    "Tired",
    "Too",
    "Traveling",
    "Trying",
    "Turning",
    "Ultimately",
    "Unafraid",
    "Under",
    "Underneath",
    "Understanding",
    "Undeterred",
    "Unexpected",
    "Unfortunately",
    "Unsure",
    "Unwilling",
    "Upon",
    "Using",
    "We",
    "What",
    "Where",
    "Whether",
    "Why",
    "Within",
    "You",
    "Armed",
    "Believing",
    "Below",
    "Berserk",
    "Bewildered",
    "Blithely",
    "Blundering",
    "Bringing",
    "Brutal",
    "Climbing",
    "Columns",
    "Covered",
    "Days",
    "Deeply",
    "Doubles",
    "Down",
    "Dozens",
    "Drunk",
    "Enduring",
    "Eyeing",
    "Falling",
    "Fine",
    "Following",
    "Frozen",
    "Fully",
    "Furious",
    "Further",
    "Gently",
    "Greeting",
    "Growing",
    "Guiding",
    "Half-delirious",
    "Handing",
    "Heavy",
    "Knowing",
    "Look",
    "Many",
    "Marching",
    "Maybe",
    "Mollified",
    "Most",
    "Quick",
    "Saddened",
    "Seeing",
    "Seizing",
    "Sensing",
    "Shaken",
    "Shielded",
    "Sick",
    "Sitting",
    "Slightly",
    "Smiling",
    "Sneering",
    "Speaking",
    "Spotting",
    "Stating",
    "Steeling",
    "Stepping",
    "Taking",
    "Teasing",
    "Telling",
    "Terrified",
    "Then",
    "Thoughtful",
    "Thousands",
    "Tied",
    "Tiring",
    "Two",
    "Undaunted",
    "Unknown",
    "Wounded",
    "Second"
    "Present-day",
    "Off-screen",
    "Three"
}


def get_lines_by_section(file):
    lines_by_section = OrderedDict()
    current_section = None
    for line in file:
        if not line.strip():
            continue

        if line.startswith("<") and line.endswith(">\n"):
            current_section = line[1:-2]
            lines_by_section[current_section] = []
            continue

        line = line.replace(u"\u00A0", " ")
        lines_by_section[current_section].append(line.strip())

    return lines_by_section


def sentence_text(sentence):
    text = ""
    for word in sentence:
        if word[0] == "'s" or word[0] == "'":
            text += word[0]
        else:
            text += " " + word[0]
    return text[1:]


def sentence_without_tag(sentence):
    return [word[0] for word in sentence]


def is_complement(word):
    text = word[0]
    return text in ("of", "the", "'s", "'")


def is_first_letter_upper(word):
    text = word[0]
    return text[0].isupper()


def remove_unfinished_complements(ne):
    ne_without_trailing_complements = list(ne)
    for i in range(len(ne) - 1, 0, -1):
        if is_complement(ne[i]):
            ne_without_trailing_complements = ne_without_trailing_complements[:-1]
        else:
            break
    return ne_without_trailing_complements


def extract_entities_from_line(line):
    sentence = nltk.word_tokenize(line)
    sentence = nltk.pos_tag(sentence)

    named_entities = []
    tokens = []

    for j, tagged_word in enumerate(sentence):

        if is_first_letter_upper(tagged_word) and not tagged_word[0] in blacklisted_words:
            tokens.append(tagged_word)

            if j != len(sentence) - 1:
                continue

        if tokens and is_complement(tagged_word) and not tagged_word[0] in blacklisted_words:
            tokens.append(tagged_word)
            if j != len(sentence) - 1:
                continue

        if tokens:
            tokens = remove_unfinished_complements(tokens)
            entity_name = sentence_text(tokens)

            en = EN(entity_name)
            en.sentence = sentence_text(sentence)
            if entity_name not in blacklisted_entities:
                named_entities.append(en)

            tokens.clear()

    return named_entities


def find_position_on_line(entities, line):
    entities_with_position = []
    for en in sorted(entities, key=lambda _: len(_.original), reverse=True):
        for match in re.finditer(en.original, line):
            new_en = EN(en.original)
            new_en.sentence = en.sentence
            new_en.start_index = match.start()
            new_en.end_index = match.end()
            entities_with_position.append(new_en)
        line = line.replace(en.original, "X"*len(en.original))

    return entities_with_position


def extract_entities_from_episode(file):
    lines_by_section = get_lines_by_section(file)
    entities_by_section = OrderedDict()

    for section in lines_by_section.keys():
        entities_by_section[section] = []

        for i, line in enumerate(lines_by_section[section]):
            entities = extract_entities_from_line(line)

            whitelist_en = [EN(name) for name in whitelist]
            entities = find_position_on_line(entities + whitelist_en, line)

            for en in entities:
                en.line = i

            entities_by_section[section].append(entities)

    return entities_by_section


def main():
    # episodes = glob.glob("episodesTXT/season_1/fire_and_blood.txt")
    # episodes = glob.glob("episodesTXT/season_1/*.txt")
    episodes = glob.glob("episodesTXT/*/*.txt")
    # episodes = glob.glob("episodesTXT/season_6/the_door.txt")

    if len(episodes) == 0:
        print("Nenhum arquivo encontrado...")
        exit()

    all_en = []
    for episode in episodes:
        season = os.path.basename(os.path.dirname(episode))
        name = os.path.basename(episode)[:-4]

        with open(episode, 'r', encoding='utf-8') as file:
            entities_by_section = extract_entities_from_episode(file)
            for section in entities_by_section.keys():
                for line in entities_by_section[section]:
                    for en in line:
                        en.episode = name
                        en.season = season
                        all_en.append(en)

        print("Finished {0}.".format(name))

        json_to_export = OrderedDict()
        for section in entities_by_section.keys():
            json_to_export[section] = []
            for line in entities_by_section[section]:
                for en in line:
                    json_to_export[section].append([en.line, en.start_index, en.end_index, en.classification.upper(), en.original])

        output_season = os.path.join("entitiesTXT", season)
        output_file = os.path.join(output_season, name + "_entities.json")
        if not os.path.exists(output_season):
            os.mkdir(output_season)
        with open(output_file, "w+") as file:
            file.write(json.dumps(json_to_export, indent=True, sort_keys=True))

    save_csv_for_debug(all_en)
    print(len(all_en))


def save_csv_for_debug(ens):
    with open("all_en.csv", "w+", encoding="utf-8") as file:
        for en in sorted(list(set(ens))):
            file.write("{0},\"{1}\",\"{2}\",\"{3}\"\n".format(en.original, en.sentence, en.episode, en.season))
            # file.write("{0}\n".format(en.original))


if __name__ == "__main__":
    main()

    # with open("entitiesTXT\\season_1_manual_markup\\fire_and_blood_entities.json") as file:
    #     content = json.load(file)
    # with open("all_en_original.csv", "w+", encoding="utf-8") as file:
    #     json.dump(content, file, indent=True, sort_keys=True)

    # episodes = glob.glob("entitiesTXT/season_1_manual_markup/*.json")
    # names = []
    # for episode in episodes:
    #     with open(episode, 'r', encoding="utf-8") as file:
    #         data = json.load(file)
    #         for section in data.keys():
    #             ens = data[section]
    #             for en in ens:
    #                 name = en[4]
    #                 names.append(name)
    #
    # with open("season_1_manual_markup.csv", "w+", encoding="utf-8") as file:
    #     for name in sorted(list(set(names))):
    #         file.write("{0}\n".format(name))
