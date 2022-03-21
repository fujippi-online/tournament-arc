import random

import props
import geometry

class MistyUndercoat:
    def update(self, scene):
        if random.random() < 0.1:
            possible_positions = list(geometry.iter_circle_border(
                scene.hero.position, scene.vision_range +2))
            centre = random.choice(possible_positions)
            for pos in geometry.iter_circle(centre, 3):
                mist = props.Mist(*pos, random.randint(10,20))
                scene.foreground.append(mist)
