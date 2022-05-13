import os
from bs4 import BeautifulSoup

PARTICIPANTS = [

    "Tai Swet Geok",
    "Lim Chek Boon",
    "Liu Qingqun",
    "Desmond Yao",
    "Hair Wen Quan Ricky",
    "Christina Ng",
    "Chiok Pei Yu",
    "Muhammad Mubarak s/o Syed Ahmad",
    "Ernest Ng Er Rui",
    "Kwong Kok Chan",
    "Lim Dao Xian",
    "Chieng chiew sek",
    "Andy Chew Hesheng",
    "Chia Hon Kit",
    "GOH YI HUI",
    "Co Hao Zhong James",
    "Daniel Shi Chee Sing",
    "Lee Jen Xiong",
    "WU HONG YU",
    "Mani Rajasekaran",
    "Samuel Har Enqi",
    "Ervin Yeo",
    "Muhammad Nur Aiman",
    "Toh Aik Meng",
    "Chen Churong",
    "Kwang Sai Weng",
    "Pey Jin Yong",
    "Gregory Tan",
    "Issac Gwee",
    "Goh Soon Hua",
    "Ethan Lim",
    "Alex Lee",
    "Faayiz Firros",
    "Lye Han Wei",
    "ERIC KOH",
    "Lee Wei Zhi Jonathan",
    "Bhashyakarla Divya",
    "Lucy Tan",
    "Wong Nyuk Ling",
    "Gan Wei Chun",
    "Ivan Lee",
    "Ho Pui Jee",
    "Boey sin yee",
    "Tan Sean",
    "Chester Chua Chee Siong",
    "Tan Jing Han Chad",
    "CHUA XIAN ZHONG",
    "Lee Jun Yi, Joshua",
    "Tan Inn Fung",
    "Lim Teck Woon, Darren",
    "TAN CHIN HOUW BENJAMIN",
    "Gilbert Lim",
    "Teo Yong Jie",
    "Tan Li Min Krystle",
    "Wang Ngiap Weng",
    "Zhao Taige",
    "Mak Hui Ting Clarisse",
    "Ng Kang Xiu Joshua",
    "TAY ZHI WEI",
    "Gu Miaoheng Raymond",
    "Cheow Eng Ho",
    "Kwek Li Gek",
    "Lee Xuanyun Calista",
    "Chua Charn Hao, Wilson",
    "Benjamin Chua Rui Hern",
    "Kok Yong Leonard Lee",
    "Zeng Jiancheng",
    "Philip Ng",
    "Ang Siok Teng Serene",
    "Lee Chin Leong",
    "Tan kuan wee",
    "Tan Kiat Seng",
    "Ong min lwin",
    "Chiang chee pun",
    "Lee Jia Wei",
    "Sng Shao Perng",
    "Garrick Goh",
    "Khoo Kai Yun Kelvin",
    "Kelvin Loh Wei Keong",
    "Law Bee Hua",
    "LIAU YEE XIANG",
    "Ng Koh Yew",
    "Tay Lim Hock",
    "Sean Lai Kuok Shen",
    "Shi Chee Yeong, John",
    "Lum Jin Xian",
    "Andre Thong",
    "Christopher Anthony",
    "Ong Jun Heng, James",
    "Alan Maguicay",
    "Ng Choong Hwee",
    "Angie Ang",
    "Wong ray mern peter",
]
PLIST_DIR = os.path.join("PlistHtml")
PLIST_FILE_NAMES = os.listdir(PLIST_DIR)


def get_names_that_matches_participants() -> dict:

    attendees_set = set()

    for plist_file_name in PLIST_FILE_NAMES:
        plist_file = os.path.join(PLIST_DIR, plist_file_name)

        if os.path.isfile(plist_file):
            with open(plist_file, 'r') as stream:
                html_soup = BeautifulSoup(stream, features="html.parser")

                [attendees_set.add(tag.string) for tag in html_soup.find_all(
                    class_="style-title-2qhbq")]

    attendees_list = list(attendees_set)
    attendees_list.sort()

    present_participants_dict = {}

    for participant in PARTICIPANTS:
        name_segments = participant.split(' ')

        for segment in name_segments:
            if len(segment) > 3:
                for attendee in attendees_list:
                    if segment.lower() in attendee.lower():
                        present_participants_dict[participant].add(
                            attendee
                        ) if participant in present_participants_dict else present_participants_dict.update(
                            {participant: set([attendee])}
                        )

    for participant, _ in present_participants_dict.items():
        present_participants_dict[participant] = list(
            present_participants_dict[participant])
        present_participants_dict[participant].sort()

    return present_participants_dict
