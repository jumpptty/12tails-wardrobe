"""The Penguin's candidate LAYOUTS (plans/fx_penguin/parts.md): each script's serialized (public) fields in declaration order."""
PENGUIN = {
    "Penguin_tornado": [("mLv", "i"), ("nPosition", "v3"), ("nVelocity", "v3")],        # Penguin_tornado.cs:605, :635, :638
    "Penguin_typhoon": [("mLv", "i"), ("nPosition", "v3"), ("nVelocity", "v3")],        # Penguin_typhoon.cs:515, :557, :560
    "Penguin_arcticEmperor": [("MinAlpha", "f"), ("MaxAlpha", "f"), ("MinEmission", "f"), ("MaxEmission", "f"),
                              ("FadeDelay", "f"), ("FadeEaseIn", "f"), ("FadeMiddle", "f"), ("FadeEaseOut", "f")],   # Penguin_arcticEmperor.cs:225-246
    "Penguin_iceBlock": [("mLife", "i"), ("mLv", "i")],                                 # Penguin_iceBlock.cs:264, :267
    "Penguin_cosmicFriday": [], "Penguin_nAttack": [], "Penguin_manaMissile": [], "Penguin_snowMan": [], "Penguin_snowBall": [],
}
