#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

from generateM3Library import generateM3Library
generateM3Library()

import m3
import sys
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make a model use the same animation ids like another model(works only for bones with the same name yet)')
    parser.add_argument('animIdFile', help="m3 with the wanted animation ids")
    parser.add_argument('modelToFix', help="m3 which has the wrong animation ids")
    parser.add_argument('outputFile', help="name of the new m3 file to create")
    args = parser.parse_args()


    animIdModel = m3.loadModel(args.animIdFile) 
    modelToFix = m3.loadModel(args.modelToFix)
    outputFile = args.outputFile

    boneNameToAnimIdBoneMap = {}
    for bone in animIdModel.bones:
        boneNameToAnimIdBoneMap[bone.name] = bone

    oldAnimIdToNewAnimIdMap = {}
    for boneToFix in modelToFix.bones:
        boneWithAnimId = boneNameToAnimIdBoneMap[boneToFix.name]
        oldAnimId = boneToFix.location.header.animId
        newAnimId = boneWithAnimId.location.header.animId
        oldAnimIdToNewAnimIdMap[oldAnimId] = newAnimId
        oldAnimId = boneToFix.rotation.header.animId
        newAnimId = boneWithAnimId.rotation.header.animId
        oldAnimIdToNewAnimIdMap[oldAnimId] = newAnimId
        oldAnimId = boneToFix.scale.header.animId
        newAnimId = boneWithAnimId.scale.header.animId
        oldAnimIdToNewAnimIdMap[oldAnimId] = newAnimId
    
    for stc in modelToFix.sequenceTransformationCollections:
        animIds = stc.animIds
        for i in range(len(animIds)):
            newAnimId = oldAnimIdToNewAnimIdMap.get(animIds[i])
            if newAnimId != None:
                animIds[i] = newAnimId
    
    for sts in modelToFix.sts:
        animIds = sts.animIds
        for i in range(len(animIds)):
            newAnimId = oldAnimIdToNewAnimIdMap.get(animIds[i])
            if newAnimId != None:
                animIds[i] = newAnimId
    
    m3.saveAndInvalidateModel(modelToFix, outputFile)

