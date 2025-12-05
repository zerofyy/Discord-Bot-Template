import pyemojify


class Emoji:
    """ Static class for consistent use of emojis. """

    fy: callable = pyemojify

    blank: str = '<:ee:1105122910051508225>'
    success: str = '<:ee:1105122920159772784>'
    denied: str = '<:ee:1105122927554338960>'
    warning: str = '<:ee:1105509639778467883>'
    error: str = '<:ee:1105122928892334111>'
    danger: str = '<:ee:1361780268792549537>'
    info: str = '<:ee:1105509087896146071>'
    question: str = '<:ee:1105122980759081030>'
    loading: str = '<a:ae:1105122946063794246>'

    command: str = '<:ee:1105509426909171833>'
    language: str = '<:ee:1105122942746112151>'
    time: str = '<:ee:1105509039443562577>'
    pen: str = '<:ee:1105509318247325736>'
    lock: str = '<:ee:1105509322571653251>'
    gear: str = '<:ee:1105509424140918815>'
    reload: str = '<:ee:1105509421494313090>'
    label: str = '<ee:1105509554323734569>'
    upload: str = '<:ee:1105122910051508225>'
    download: str = '<:ee:1105508991620087869>'
    delete: str = '<ee:1105509564809490614>'
    missing: str = '<:ee:1105509041964327003>'
    globe: str = '<:ee:1105509047140102215>'
    link: str = '<:ee:1105509089129283634>'
    user: str = '<:ee:1105509635408019527>'
    like: str = '<:ee:1105122994587697172>'
    dislike: str = '<ee:1105509548460089395>'

    class ping:
        """ Static subclass for latency status emojis. """

        good: str = '<:ee:1105122977206517890>'
        okay: str = '<:ee:1105509430415597649>'
        bad: str = '<:ee:1105509319719534682>'

    class progress:
        """ Static subclass for progress bar segment emojis. """

        seg_null_l: str = '<:ee:1106587508596285552>'
        seg_half_l: str = '<:ee:1106587505798693025>'
        seg_full_l: str = '<:ee:1106587503546347630>'
        seg_null_m: str = '<:ee:1106587500983635968>'
        seg_half_m: str = '<:ee:1106587499540783244>'
        seg_full_m: str = '<:ee:1106587497284243579>'
        seg_null_r: str = '<:ee:1106587496055324682>'
        seg_half_r: str = '<:ee:1106587494700548126>'
        seg_full_r: str = '<:ee:1106587491777126461>'
        seg_none_u: str = '▱▱'
        seg_half_u: str = '▰▱'
        seg_full_u: str = '▰▰'

    class unicode:
        """ Static subclass for unicode emojis. """

        reply = '⤷'


__all__ = ['Emoji']
