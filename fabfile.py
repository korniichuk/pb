#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name: pb

from fabric.api import local


def git():
    """Configure Git"""

    local("git remote rm origin")
    local("git remote add origin "
          "https://korniichuk@github.com/korniichuk/pb.git")
