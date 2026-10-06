# RAC W1h: ordinary-rule (AD-G10) re-check of the saved thoracic-breadth probe bodies T0-T4, T6, T7 (reference body only)
import sys; sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1h_drivers'); import gn5, gn3
for n in ('PTT0', 'PTT1', 'PTT2', 'PTT3', 'PTT4', 'PTT6', 'PTT7'):
    rows = gn3.checks('GO', n, wd=gn5.G + '/solve5')
    print(n, 'ORDINARY RULE not-pass:', [(y['result'], y['check'][:70]) for y in rows if (y['cand'] == 'GO' or y.get('b') == 'GO') and y['result'] not in ('PASS', 'REPORT', 'NOT RUN')], flush=True)
