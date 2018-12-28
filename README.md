SysyphOS
========

Last updated 2018-10-21.

This toy project aims to build a self-reliant operating system on it's
own programming language with it's own compiler running in that
operating system.

Table of contents
-----------------

- [1. Implementation steps](#implementation-steps)
  - [1.1 Requirements](#11-requirements)
  - [1.2 Bootstraping](#12-bootstraping)
  - [1.3 Kernel](#13-kernel)
  - [1.4 Shell](#14-shell)
  - [1.5 Editor](#15-editor)
- [2. The Kore Programming Language](#2-the-kore-programming-language)
  - [2.1 Data Types](#21-data-types)
  - [2.2 Comparison operators](#22-comparison-operators)
  - [2.3 Assign](#23-assign)
  - [2.4 Arithmetic operators](#24-arithmetic-operators)
  - [2.5 Flow control](#25-flow-control)
  - [2.6 Declarations](#26-declarations)
  - [2.7 Example](#27-example)
- [3. Kore interpreter, korerun.py](#3-kore-interpreter-korerunpy)
- [4. Kore standard library](#4-core-standard-library)
- [5. Kore compiler](#5-kore-compiler)
- [6. SysyphOS kernel](#6-sysyphos-kernel)
- [7. SysyphOS shell](#7-sysyphos-shell)
- [8. SysyphOS editor](#8-sysyphos-editor)
- [9. References](#9-references)

1 Implementation steps
======================

1.1 Requirements
----------------

The requirements deceptively are simple to describe:
- The operating system must compile itself and be self-modificable
  The edit-compile-test cycle must be self-hosted. No cross compilers,
  no existing languages (i.e. C)
- The programing language must be just enough to express the operating
  system and compiler for itself on it.
- The compiler for the language will be written in the language itself.

1.2 Bootstraping
----------------

Bootstraping process:

- Kore interpreter written in python
- Kore compiler written in Kore
- Compile Kore running the Kore interpreter over the
  Kore compiler code

1.3 Kernel
----------

Write the SysyphOS kernel in Kore

1.4 Shell
---------

Write some kind of shell to be able to run the compiler and editor

1.5 Editor
----------

Barebones code editor to be able to self-modify the SysyphOS code in
itself

2 The Kore programming language
===============================

Somehow resembles lisp and uses s-expressions, but it is purely
procedural and as simple as it can be to ease implementation.

2.1 Data Types
--------------

Three integer types are provided:

- Word  (16 bits)
- Dword (32 bits)
- Byte (8 bits)

A pointer type

- Memory address (arch dependent)

Inmediate values with types:

- Inmediate string     "inmediate string"
- Inmediate word       10w
- Inmediate byte       10b
- Inmediate dword      10d
- Inmediate character  'c' (always byte)

2.2 Comparison operators
------------------------

Only three comparison operators are provided, working only on integer
types

- gt (Greather than)
- eq (Equal)
- lt (Less than)

2.3 Assign
----------

set

2.4 Arithmetic operators
------------------------

Arithmetic operators only work on integer types

- add
- minus
- mul
- div

2.5 Flow control
----------------

Three flow control operators:

- if
- while
- return

2.6 Declarations
----------------

Those declare functions, variables and complex structures

- function
- declare

2.7 Example
-----------

```
(program "Example"
  (function hello
    (print "Hello world"))

  (function hello-what what
    (print (add "Hello " what)))

  (declare word i)
  (declare address p)

  (set p (address i))
  (add 5w 10w 15w)

  (if (gt 5w 10w)
    (print "One")
    (print "Two"))

 (set i 0w)
 (while (lt iw 10w)
   (print "iteration")
   (set i (add 1w i)))

 (hello)
 (hello-what "what"))
```

3 Kore interpreter: korerun.py
==============================

The Kore Interpreter, korerun.py runs on Python version 3.5
onwards. It implements enough of the Kore language to
implement the kore compiler

4 Kore standard library
=======================

Needs to be implemented both in the interpreter, in the compiler and
in the target S.O.

5 Kore compiler
===============

Wip

6 SysyphOS kernel
=================

Wip

7 SysyphOS shell
================

Wip

8 SysyphOS editor
=================

Wip

9 References
============

These are small lisp interpreters, compilers and operating system
writing references that I find useful.

- [Step by step to MIPS assembly](http://winfred-lu.blogspot.com/2010/06/step-by-step-to-mips-assembly.html)
- [Lisp in less than 200 lines of C](https://carld.github.io/2017/06/20/lisp-in-less-than-200-lines-of-c.html)
- [Lispy](http://norvig.com/lispy.html)
