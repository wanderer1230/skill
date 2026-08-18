#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probe.py — 本 skill 的唯一脚本,两种模式。

  模式 A  --recon        仓库测绘。整个项目只跑一次。
  模式 B  --anchors FILE  锚点取证。按业务对象批量取证,一次跑完所有锚点。

设计目标是把脚本调用次数压到最低:一次 recon + 一到两次 anchors,
覆盖全部机械提取工作。两种模式都只对仓库做一次遍历。

不依赖 git、不依赖网络、纯标准库。优先级判断用文件 mtime + 引用计数。

锚点文件格式(每行一个业务对象,# 开头为注释):

    批次 = TO_BATCH, BATCH_ID, batchNo, PC
    光罩订单 = MASK_ORDER, MO_, MaskOrder, GZDD
    DRC签核 = SIGNOFF, DRC, signoffFlag

左边是业务名(你已知的),右边是它在代码里可能的写法(别名/表名/前缀)。
别名宁滥勿缺 —— 命中噪音可以人工剔除,漏掉了就整条业务线断在这里。
"""
import argparse
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict

ENCODINGS = ('utf-8', 'gb18030', 'gbk', 'latin-1')
SKIP_DIRS = {'.git', '.svn', 'node_modules', 'target', 'build', 'dist',
             '.idea', '.settings', '__pycache__'}
CODE_EXT = ('.java', '.jsp', '.jspf', '.xml', '.properties', '.sql', '.js',
            '.logic', '.bizlogic', '.biz', '.dao', '.entity', '.cmpt',
            '.flow', '.pageflow', '.wf', '.bpmn', '.ddl', '.vm', '.ftl')
CN_RE = re.compile(r'[\u4e00-\u9fff]')


# ---------- 公共 ----------

def read_text(path):
    """老系统 GBK 常见。逐编码试,别让一个乱码文件中断整轮。"""
    try:
        with open(path, 'rb') as f:
            raw = f.read()
    except Exception:
        return None, None
    for enc in ENCODINGS:
        try:
            return raw.decode(enc), enc
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode('utf-8', 'replace'), 'utf-8-replace'


def walk(root, exts=CODE_EXT):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.lower().endswith(exts):
                yield os.path.join(dirpath, fn)


def lineno(text, pos):
    return text.count('\n', 0, pos) + 1


def ctx(text, pos, before=90, after=110):
    s = text[max(0, pos - before):pos + after]
    return re.sub(r'\s+', ' ', s).strip()


def age_days(path):
    try:
        return int((time.time() - os.path.getmtime(path)) / 86400)
    except Exception:
        return -1


# ---------- 模式 A: recon ----------

ROOT_TAG_RE = re.compile(r'<([A-Za-z][\w:.-]*)[\s/>]')
COORD_RE = re.compile(r'\b(?:x|y|posX|posY)\s*=\s*"[-\d]+"')
CMPT_RE = re.compile(r'(component\.xml|\.cmpt|contract\.xml|package\.xml)$', re.I)
DEAD_RE = re.compile(
    r'/(bak|backup|old|obsolete|deprecated|unused|copy|备份)[\w-]*/|'
    r'_(19|20)\d{2}[01]\d([0-3]\d)?/', re.I)


def do_recon(root, out):
    ext_c, roottag_c, enc_c, coord_ext = Counter(), Counter(), Counter(), Counter()
    coord_samples, cmpt_dirs, dead_dirs = {}, set(), Counter()
    dir_files, dir_newest = Counter(), {}
    total = 0

    for path in walk(root, exts=None if False else CODE_EXT):
        total += 1
        ext = os.path.splitext(path)[1].lower()
        ext_c[ext] += 1
        d = os.path.dirname(path)
        dir_files[d] += 1
        a = age_days(path)
        if a >= 0:
            dir_newest[d] = min(dir_newest.get(d, 10 ** 9), a)
        if CMPT_RE.search(path):
            cmpt_dirs.add(d)
        if DEAD_RE.search(path.replace(os.sep, '/')):
            dead_dirs[d] += 1

        if ext in ('.xml', '.logic', '.bizlogic', '.biz', '.flow', '.pageflow',
                   '.wf', '.bpmn', '.dao', '.entity', '.cmpt'):
            text, enc = read_text(path)
            if text is None:
                continue
            enc_c[enc] += 1
            m = ROOT_TAG_RE.search(text[:6000])
            if m:
                roottag_c['%s  <%s>' % (ext, m.group(1))] += 1
            # 带坐标 = 可视化编辑器画出来的 = 编排文件。最可靠的判据。
            if COORD_RE.search(text[:40000]):
                coord_ext[ext] += 1
                coord_samples.setdefault(ext, path)
        elif ext in ('.java', '.jsp', '.properties', '.sql'):
            _, enc = read_text(path)
            if enc:
                enc_c[enc] += 1

    # 顶层目录聚合
    top = Counter()
    for d, n in dir_files.items():
        rel = os.path.relpath(d, root).split(os.sep)[0]
        top[rel] += n

    res = {
        'mode': 'recon',
        'root': root,
        'total_code_files': total,
        'ext_distribution': ext_c.most_common(40),
        'xml_root_tags': roottag_c.most_common(30),
        'ORCHESTRATION_CANDIDATES': {
            'note': '带坐标属性的文件几乎必然是可视化编排产物。'
                    '认定编排扩展名请以此为准,并抽样打开 sample 确认。',
            'by_ext': coord_ext.most_common(),
            'samples': coord_samples,
        },
        'encoding_distribution': enc_c.most_common(),
        'ENCODING_WARNING': ('检测到非 UTF-8,后续所有读取必须显式指定编码,'
                             '否则中文术语全部作废'
                             if any(e in ('gbk', 'gb18030', 'utf-8-replace')
                                    for e, _ in enc_c.items()) else None),
        'top_level_dirs': top.most_common(30),
        'component_package_dirs': sorted(cmpt_dirs)[:60],
        'suspected_dead_dirs': dead_dirs.most_common(25),
        'staleness_by_dir': sorted(
            [(v, k, dir_files[k]) for k, v in dir_newest.items()],
            reverse=True)[:30],
        'staleness_note': ('无 git 时用 mtime 代替改动频次。'
                           '第一列是该目录内最新文件的"天数龄",数值大 = 长期未动 = '
                           '疑似死代码线索。仅为线索,静态分析不能确认废弃。'),
    }
    dump(res, out)


# ---------- 模式 B: anchors ----------

def parse_anchors(path):
    anchors = {}
    text, _ = read_text(path)
    if text is None:
        sys.exit('无法读取锚点文件: %s' % path)
    for i, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            print('第 %d 行缺少 "=",已跳过: %s' % (i, line), file=sys.stderr)
            continue
        name, rest = line.split('=', 1)
        aliases = [a.strip() for a in re.split(r'[,，]', rest) if a.strip()]
        if aliases:
            anchors[name.strip()] = aliases
    return anchors


# 每类命中用一组模式识别,目的是把"出现"升级为"出现在什么语境"
# 顺序即优先级:先判定信息量大的语境(DDL / 写库 / 常量定义),
# 再回落到弱语境。每条模式都必须绑定锚点别名 %s,否则会把无关代码
# 误标成该锚点的写入点 —— 这类误标会直接污染状态机的边。
KIND_PATTERNS = [
    ('ddl', re.compile(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"\[]?\w*%s\w*', re.I)),
    ('sql_write', re.compile(
        r'\b(?:UPDATE|INSERT\s+INTO|DELETE\s+FROM)\s+[`"\[]?\w*%s\w*|'
        r'\bSET\b[^;]{0,120}?\w*%s\w*\s*=', re.I)),
    ('const_def', re.compile(r'static\s+final\s+\w+\s+\w*%s\w*\s*=', re.I)),
    ('field_write', re.compile(r'\.\s*set\w*%s\w*\s*\(', re.I)),
    ('field_read', re.compile(r'\.\s*get\w*%s\w*\s*\(', re.I)),
    ('sql_read', re.compile(r'\b(?:FROM|JOIN)\s+[`"\[]?\w*%s\w*', re.I)),
    ('xml_ref', re.compile(r'<[^>]*\b\w*%s\w*\b[^>]*>', re.I)),
]
MSG_RE = re.compile(
    r'(?:throw\s+new\s+\w*(?:Exception|Error)\w*|addError|addMessage|alert|'
    r'setErrMsg|setErrorMsg)\s*\([^;]{0,240}', re.I)
STR_LIT_RE = re.compile(r'"((?:[^"\\]|\\.){2,200})"')
COND_RE = re.compile(r'(?:condition|expr|expression|test|when)\s*=\s*"([^"]{1,200})"', re.I)
IF_RE = re.compile(r'\bif\s*\(([^{;]{3,200})\)')
CONST_ANY_RE = re.compile(
    r'static\s+final\s+(?:String|int|Integer|char)\s+([A-Z][A-Z0-9_]{2,})\s*=\s*'
    r'("(?:[^"\\]|\\.)*"|-?\d+)')


def do_anchors(root, anchor_file, out, max_hits, ctx_lines):
    anchors = parse_anchors(anchor_file)
    if not anchors:
        sys.exit('锚点文件为空')

    # 为每个别名预编译
    alias_re = {}
    for name, aliases in anchors.items():
        for al in aliases:
            alias_re.setdefault(al, re.compile(re.escape(al), re.I))

    hits = {n: defaultdict(list) for n in anchors}
    file_count = {n: Counter() for n in anchors}
    cooccur = Counter()
    constants = []
    messages = defaultdict(list)
    conditions = defaultdict(list)
    scanned = 0

    for path in walk(root):
        text, enc = read_text(path)
        if text is None:
            continue
        scanned += 1
        present = set()

        for name, aliases in anchors.items():
            n_here = 0
            for al in aliases:
                for m in alias_re[al].finditer(text):
                    n_here += 1
                    if n_here > max_hits:
                        break
                    ln = lineno(text, m.start())
                    line_txt = ctx(text, m.start())
                    kind = 'mention'
                    for kname, kpat in KIND_PATTERNS:
                        try:
                            esc = re.escape(al)
                            pat = kpat.pattern % ((esc,) * kpat.pattern.count('%s'))
                            if re.search(pat, line_txt, re.I):
                                kind = kname
                                break
                        except (re.error, TypeError):
                            pass
                    hits[name][kind].append({
                        'alias': al,
                        'evidence': '%s:%d' % (path, ln),
                        'context': line_txt[:220],
                    })
                if n_here:
                    present.add(name)
                    file_count[name][path] += n_here
            if n_here:
                # 该文件里与本锚点同处的错误文案 / 条件表达式
                for m in MSG_RE.finditer(text):
                    lit = STR_LIT_RE.search(m.group(0))
                    if lit and (CN_RE.search(lit.group(1)) or len(lit.group(1)) > 6):
                        messages[name].append({
                            'message': lit.group(1),
                            'evidence': '%s:%d' % (path, lineno(text, m.start())),
                        })
                for m in COND_RE.finditer(text):
                    conditions[name].append({
                        'expr': m.group(1),
                        'evidence': '%s:%d' % (path, lineno(text, m.start())),
                        'src': 'xml',
                    })
                for m in IF_RE.finditer(text):
                    e = m.group(1).strip()
                    if any(alias_re[al].search(e) for al in anchors[name]):
                        conditions[name].append({
                            'expr': e[:200],
                            'evidence': '%s:%d' % (path, lineno(text, m.start())),
                            'src': 'java/jsp',
                        })

        # 共现 = 数据流的候选证据
        pl = sorted(present)
        for i in range(len(pl)):
            for j in range(i + 1, len(pl)):
                cooccur[(pl[i], pl[j])] += 1

        for m in CONST_ANY_RE.finditer(text):
            if any(alias_re[al].search(m.group(1)) for n in anchors for al in anchors[n]):
                constants.append({
                    'name': m.group(1), 'value': m.group(2).strip('"'),
                    'evidence': '%s:%d' % (path, lineno(text, m.start())),
                })

    per_anchor = {}
    for name in anchors:
        kinds = {k: v[:60] for k, v in hits[name].items()}
        msg = []
        seen = set()
        for it in messages[name]:
            if it['message'] not in seen:
                seen.add(it['message'])
                msg.append(it)
        conds, cseen = [], set()
        for it in conditions[name]:
            if it['expr'] not in cseen:
                cseen.add(it['expr'])
                conds.append(it)
        per_anchor[name] = {
            'aliases': anchors[name],
            'total_hits': sum(len(v) for v in hits[name].values()),
            'hit_kinds': {k: len(v) for k, v in hits[name].items()},
            'top_files': [{'file': f, 'hits': c, 'stale_days': age_days(f)}
                          for f, c in file_count[name].most_common(15)],
            'evidence_by_kind': kinds,
            'messages': msg[:40],
            'conditions': conds[:60],
        }

    weak = [n for n, v in per_anchor.items() if v['total_hits'] == 0]

    res = {
        'mode': 'anchors',
        'files_scanned': scanned,
        'anchors': list(anchors),
        'ZERO_HIT_ANCHORS': weak,
        'zero_hit_note': ('命中为 0 说明别名给错了,或该业务不在本系统实现。'
                          '两种可能含义完全不同,必须区分后再继续 —— '
                          '直接当作"系统没有这个功能"是典型误判。'),
        'cooccurrence': [{'pair': list(k), 'files': v}
                         for k, v in cooccur.most_common(80)],
        'cooccurrence_note': ('共现次数高 = 两个业务对象在代码里紧密耦合,'
                              '是数据流的候选证据。但共现只证明"有关系",'
                              '不证明方向;方向要回到 evidence 位置读读写语义。'),
        'constants': constants[:200],
        'per_anchor': per_anchor,
    }
    dump(res, out)


def dump(obj, out):
    js = json.dumps(obj, ensure_ascii=False, indent=2)
    if out == '-':
        sys.stdout.write(js)
    else:
        d = os.path.dirname(os.path.abspath(out))
        if d:
            os.makedirs(d, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(js)
        print('written: %s (%.0f KB)' % (out, len(js) / 1024), file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('root', help='代码库根路径')
    ap.add_argument('--recon', action='store_true', help='模式 A:仓库测绘')
    ap.add_argument('--anchors', metavar='FILE', help='模式 B:锚点文件路径')
    ap.add_argument('--out', default='-', help='输出 JSON 路径,默认 stdout')
    ap.add_argument('--max-hits', type=int, default=200,
                    help='单文件单锚点最大命中数,防止一个巨型文件淹没结果')
    ap.add_argument('--ctx', type=int, default=1, help='保留参数')
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        sys.exit('路径不存在: %s' % args.root)
    if args.recon:
        do_recon(args.root, args.out)
    elif args.anchors:
        do_anchors(args.root, args.anchors, args.out, args.max_hits, args.ctx)
    else:
        sys.exit('需指定 --recon 或 --anchors FILE')


if __name__ == '__main__':
    main()
