# -*- coding: utf-8 -*-

import argparse
from time import sleep
import colorama as cl
import csv
import random


def main(poke_list,is_debug,is_vs):
    """Main tasks.

    Args:
        poke_list (str): ポケモンのリスト (csvファイルのパス)
    """
    with open(poke_list, "r", encoding="utf-8") as f:
        r = csv.reader(f)
        pokemons = [row for row in r]

    choiced = random.choice(pokemons)
    target = {
        "name": choiced[0],
        "type_01": choiced[1],
        "type_02": choiced[2],
    }

    # 対話インタフェース
    cl.init(autoreset=True)
    if is_debug :
        print(target)
    print("help: ゲームのルールを表示する。\n")
    print("ai: AIに回答させる。\n")
    print("hint: ヒントとして正解のポケモンのタイプを表示する。\n")
    print("quit: 終了\n")
    answer = ""
    hint_count = 0 
    if is_vs:
        is_game_quit = False
        is_player_turn = False
        while answer != target["name"] and not is_game_quit:
          is_player_turn = not is_player_turn
          if is_player_turn:
            print("\nプレイヤーのターンです。回答を入力してください")
            answer = input("> ")
            if answer == "quit":
                print("正解は{}でした。".format(target["name"]))
                is_game_quit = True
            elif answer == "ai":
                sleep(1)
                answer = call_ai(pokemons)
                judge(target["name"], answer)
            elif answer == "hint":
                hint(target,hint_count)
                hint_count = 1
                is_player_turn = not is_player_turn
            elif len(answer) != 5:
                print("回答は5文字で入力してください。")
                is_player_turn = not is_player_turn
            else:
                judge(target["name"], answer)
          else:
            print("\nコンピューターのターンです")
            sleep(1)
            answer = call_ai(pokemons)
            judge(target["name"], answer)
          
        if is_game_quit:
            return 
        else :
            if is_player_turn:
              print("プレイヤーの勝利！")
            else :
              print("コンピュータの勝利！")
            return
    
    else :
      count = 0
      while answer != target["name"]:
          answer = input("> ")
          if answer == "quit":
              print("正解は{}でした。".format(target["name"]))
              return
          elif answer == "help":
              guide()
          elif answer == "ai":
              count += 1
              judge(target["name"], call_ai(pokemons))
          elif answer == "hint":
              hint(target,hint_count)
              hint_count = 1
          elif len(answer) != 5:
              print("回答は5文字で入力してください。")
          else:
              count += 1
              judge(target["name"], answer)
      print("\n{}手目で正解！".format(count))
      return


def guide():
    """Display a guide.
    ゲームのルールを表示する。
    """
    print("5文字のポケモンの名前を当てるゲームです！\n")
    print(cl.Fore.YELLOW + "文字だけ合っていたら黄色で、")
    print(cl.Fore.GREEN + "文字も位置も合っていたら緑色で、")
    print(cl.Fore.WHITE + "違っていたら白色の \"・\" で表示します。\n")

def call_ai(pokemons):
    """Make computer player to answer.
    AIに回答させる。
    Args:
        poke_list (list): ポケモンのリスト
    Returns:
        str: 回答
    """
    choiced = random.choice(pokemons)
    print(choiced[0])
    return choiced[0]

def hint(target,hint_count):
    """Display types of choiced pokemon.
    ヒントを表示させる
    Args:
        target (pokemon): 正解のポケモン 
        hint_count (int): ヒントが初めてかどうか
    Returns:
        str: ヒントの表示
    """
    if(hint_count == 0):
        print("タイプ1は" + target["type_01"] + "です。")
    else :
        if target["type_02"] == "":
             return print("タイプ1は" + target["type_01"] + "、タイプ2はありません。")
        else :
             return print("タイプ1は" + target["type_01"] + "、タイプ2は" + target["type_02"] + "です。")

def judge(target, answer):
    """Judge if the answer is correct.
    文字列が正解かどうかを判定し、結果を色付きで出力する。

    Args:
        target (str): 正解の文字列
        answer (str): 回答

    Raises:
        ValueError: targetとanswerの文字数が異なる場合
    """
    if len(target) != len(answer):
        raise ValueError("targetとanswerの文字数が一致しません。")

    remaining = []
    for c in target:
        remaining.append(c)

    # 完全一致を検出
    is_green = []
    for i in range(len(answer)):
        if target[i] == answer[i]:
            is_green.append(True)
            remaining[i] = ""
        else:
            is_green.append(False)

    # 文字だけ合っているものを検出
    is_yellow = []
    for i, c in enumerate(answer):
        if is_green[i]:
            is_yellow.append(False)
            continue
        elif c in remaining:
            is_yellow.append(True)
            remaining[remaining.index(c)] = ""
        else:
            is_yellow.append(False)

    # 色付きで出力
    print("  ", end="")
    for i, c in enumerate(answer):
        if is_green[i]:
            print(cl.Fore.GREEN + c, end="")
        elif is_yellow[i]:
            print(cl.Fore.YELLOW + c, end="")
        else:
            print(cl.Fore.WHITE + "・", end="")
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="5文字のポケモンの名前を当てるゲームです！")
    parser.add_argument("list", type=str, help="ポケモンのリスト (csvファイルのパス)")
    parser.add_argument("--debug", action="store_true", help="デバッグモードで実行する")
    parser.add_argument("--vs", action="store_true", help="コンピュータとの対戦モードで実行する")
    args = parser.parse_args()
    main(args.list,args.debug,args.vs)

