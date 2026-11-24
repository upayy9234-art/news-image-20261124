# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/upayy9234-art/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/upayy9234-art/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One program, one image: the front page of Tuesday, 24 November 2026, drawn entirely in pure Python stdlib. `main.py` hand-builds a 1024x1024 PNG — its own PNG encoder (signature, IHDR, IDAT, IEND, CRC32 on every chunk), its own 5x7 bitmap type, a burning warship at Benghazi at night, a rising market chart and a Washington column — and writes it to `entry.png`. No network, no randomness, no clock: two runs produce byte-identical output, and the program re-reads its own output and verifies every chunk CRC, the 1024x1024 dimensions and the 1 MiB size limit before exiting 0.

## The page

- **Hero — Benghazi, Libya:** Ukraine's sea drones sink the Russian corvette Merkury at the Benghazi naval base; a Ka-27 helicopter is destroyed and the cargo ship MV Angara is hit. Kyiv says the war has spilled 2,000 km from the front. (AP / Reuters / CNN, 23–24 Nov.)
- **Markets:** Wall Street roars back as Nvidia reinstates Jensen Huang as CEO — shares +31%, Nasdaq +6%, S&P 500 +5%; CrowdStrike agrees to buy Zscaler for $44bn. (Reuters / AP, 23 Nov.)
- **Washington:** The FBI's deputy director is to retire in December; Trump blocks the Army's plan to detonate bomb-making chemicals in Iowa without court approval; Democrats plan 12 debates for their 2028 primary. (Reuters / AP, 23–24 Nov.)
- **In brief:** The EU unveils sweeping new Russia sanctions on banks, crypto and sport; FIFA picks the US to co-host the 2031 Women's World Cup and the UK for 2035; the US loses its measles-free status as cases hit a decades high; Congo will halt cobalt exports from 30 November to lift prices.

## Run it

```sh
python3 main.py entry.png
```

Or, the way the grader runs it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ermzz861&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
