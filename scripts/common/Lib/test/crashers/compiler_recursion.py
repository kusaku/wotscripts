# Embedded file name: scripts/common/Lib/test/crashers/compiler_recursion.py
"""
The compiler (>= 2.5) recurses happily.
"""
compile('()' * 59049, '?', 'exec')