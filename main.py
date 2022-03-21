import adventure
import map_generators
import message
import menu
import time
import random
import core
import props
import game_time
import mon_types
import mon_species
import mons
import term_interpreter
import cast
import map_util
from title_screen import TitleScreen
from undercoat import DynamicChunkMapGen, AreaGridChunkGen
from control import takeover
from core import term
from map_scene import MapScene
from world_generation import test_city, test_forest, test_plateau
def tutorial():
        tutorial_message = [
            "Welcome to the world of MONS.",
            "Monsters are everywhere and you are one of them.",
            "Being a monster is great and fun.",
            "You are a special kind of monster.",
            "You are a COACH.",
            "You can only become stronger by making the monsters "+
            "around you become strong.",
            "Many MONs love to be strong and to FIGHT.",
            "Help the MONs that love to fight to become strong, and "+
            "succeed at the sport of competitive fighting.",
            "But be careful - you will need to build up the SELF-CONFIDENCE "+
            "of your comrades and earn their TRUST to succeed.",
            "Remember, each MON is different, and so are you.",
            "Good luck!",
            ]
        for msg in tutorial_message:
            game.show_message(msg)
def run_game():
    game = test_plateau.generate()
    adventure.current.scene = game
    adventure.current.revive_point = (game, game.hero.position)
    print(term.width, term.height)
    with term.fullscreen(), term.cbreak(), term.hidden_cursor(), term.keypad():
        game.camera.center_on(game.hero)
        game.render()
        message.log.render(term)
        takeover(TitleScreen())
        name_input = menu.InputBox("What's your name?", bg = game)
        pc_name = takeover(name_input)
        coach_species = []
        for mon_type in adventure.current.types:
            coach_species.append(
                    mon_species.Species(types=(mon_types.coach,
                        random.choice(adventure.current.types))))
        pc_menu = menu.FloatingMenu(0,0,list(
            [(f"{spe.name} {spe.description}", spe) for spe in
                coach_species]), bg = game, title = "Pick your character.")
        pc_species = takeover(pc_menu)
        partners = random.sample(adventure.current.mons, k=10)
        partner_menu = menu.FloatingMenu(0,0,list(
            [(f"{spe.name} {spe.description}", spe) for spe in
                partners]), bg = game, title = "Pick your partner.")
        partner_species = takeover(partner_menu)
        pc = mons.Mon(pc_species)
        pc.name = f"{pc.species.name} {pc_name}"
        partner = mons.Mon(partner_species)
        adventure.current.party = [partner, pc]
        party_member = cast.PartyMember(0,0,adventure.current.party[0])
        adventure.current.map_party.append(party_member)
        map_util.place_item(game, game.camera.rect, party_member)
        game.render()
        message.log.render(term)
        while True:
            adventure.current.scene.update(term_interpreter.get_signal())
            adventure.current.scene.render()
            message.log.render(term)
            if adventure.current.scene.transition_with:
                next_scene = aventure.current.scene.transition_with
                adventure.current.scene.transition_with = None
                adventure.current.scene = next_scene
                adventure.current.scene.render()
if __name__ == '__main__':
    run_game()
