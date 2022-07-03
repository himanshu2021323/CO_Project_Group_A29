import sys

opCodes = { 'add':'10000', 'sub':'10001', 'mov':'10010', 
'mov': '10011', 'ld':'10100', 'st':'10101', 'mul':'10110',
'div':'10111', 'rs':'11000', 'ls':'11001', 'xor':'11010',
'or':'11011', 'and':'11100', 'not':'11101', 'cmp':'11110',
'jmp':'11111', 'jlt':'01100', 'jgt':'01101', 'je':'01111',
'hlt':'01010'
}
lines, lineInfo, lineAdr, labels = [], [], [], {}
LINEINFO_NONE, LINEINFO_ORG, LINEINFO_BEGIN, LINEINFO_END = 0X00000, 0X10000, 0X20000, 0X40000


if len(sys.argv) != 2:
    print('usage: Assembler.py <sourcefile>')
    sys.exit(1)

file = open(sys.argv[1], 'r')
while True:
    line = file.readline()
    if not line:
        break
    lines.append(line.strip())
file.close()

for i in range(len(lines)):
    while(lines[i].find('\'')) != -1:
        k = lines[i].find('\'')
        l = lines[i].find('\'', k+1)
        if k != -1 and l != -1:
            replaced = ''
            for c in lines[i][k+1:l]:
                replaced += str(ord(c)) + ' '
            lines[i] = lines[i][0:k] + replaced + lines[i][l+1:]
        else:
            break

    if (lines[i].find(';') != -1):
        lines[i] = lines[i][0:lines[i].find(';')]
    lines[i] = lines[i].replace(',',' ')

    lineInfo.append(LINEINFO_NONE)
    if lines[i].find('#begin') != -1:
        lineInfo[i] |= LINEINFO_BEGIN
        lines[i] = lines[i].replace('#begin', '')
    if lines[i].find('#end') != -1:
        lineInfo[i] |= LINEINFO_END
        lines[i] = lines[i].replace('#end', '')
    k = lines[i].find('#org')
    if (k != -1):
        s = lines[i][k:].split()
        lineInfo[i] |= LINEINFO_ORG + int(s[1], 0)
        lines[i] = lines[i][0:k].join(s[2:])

    if lines[i].find(':') != -1:
        labels[lines[i][:lines[i].find(':')]] = i
        lines[i] = lines[i][lines[i].find(':')+1:]

    lines[i] = lines[i].split()

    for j in range(len(lines[i])-1, -1, -1):
        try:
            lines[i][j] = opCodes[lines[i][j]]
        except:
            if lines[i][j].find('0x') == 0 and len(lines[i][j]) > 4:
                val = int(lines[i][j], 16)
                lines[i][j] = str(val & 0xff)
                lines[i].insert(j+1, str((val>>8) & 0xff))

adr = 0
for i in range(len(lines)):
    for j in range(len(lines[i])-1, -1, -1):
        e = lines[i][j]
        if e[0] == '<' or e[0] == '>':
            continue
        if e.find('+') != -1:
            e = e[0:e.find('+')]
        if e.find('-') != -1:
            e = e[0:e.find('-')]
        try:
            labels[e]
            lines[i].insert(j+1, '0x@@')
        except:
            pass
    if lineInfo[i] & LINEINFO_ORG:
        adr = lineInfo[i] & 0xffff
    lineAdr.append(adr)
    adr += len(lines[i])

for l in labels:
    labels[l] = lineAdr[labels[l]]
for i in range(len(lines)):
    for j in range(len(lines[i])):
        e = lines[i][j]
        pre = ''
        off = 0
    if e[0] == '<' or e[0] == '>':
            pre = e[0]
            e = e[1:]
    if e.find('+') != -1:
        off += int(e[e.find('+')+1:], 0)
        e = e[0:e.find('+')]
    if e.find('-') != -1:
        off -= int(e[e.find('-')+1:], 0)
        e = e[0:e.find('-')]
    try:
        adr = labels[e] + off
        if pre == '<':
            lines[i][j] = str(adr & 0xff)
        elif pre == '>':
            lines[i][j] = str((adr>>8) & 0xff)
        else:
            lines[i][j] = str(adr & 0xff)
            lines[i][j+1] = str((adr>>8) & 0xff)
    except:
        pass
    try:
        int(lines[i][j], 0)
    except:
        print('ERROR in line' + str(i+1) + ': Undefined expression \'' + lines[i][j] + '\'')
        exit(1)
for i in range(len(lines)):
    s = ('%04.4x' % lineAdr[i]) + ": "
    for e in lines[i]:
        s += ('%02.2x' % (int(e, 0) & 0xff)) + ' '
    print(s)

# insert = ''
# showout = True
# for i in range(len(lines)):
#     if lineInfo[i] & LINEINFO_BEGIN:
#         showout = True
#     if lineInfo[i] & LINEINFO_END:
#         showout = False
#     if showout:
#         if lineInfo[i] & LINEINFO_ORG:
#             if insert:
#                 print(':' + insert)
#                 insert = ''
#             print('%04.4x' % (lineInfo[i] & 0xffff))
#         for e in lines[i]:
#             insert += ('%02.2x' % (int(e, 0) & 0xff)) + ' '
#             if len(insert) >= 16*3-1:
#                 print(':' + insert)
#                 insert = ''
# if insert:
#     print(':' + insert)