"""
////////////////////////////////////////////////////////////////////////////////
//
//  IDEUM
//  Copyright 2011-2013 Ideum
//  All Rights Reserved.
//
//  Gestureworks Core
//
//  File:    GWCUtils.py
//  Authors:  Ideum
//
//  NOTICE: Ideum permits you to use, modify, and distribute this file only
//  in accordance with the terms of the license agreement accompanying it.
//
////////////////////////////////////////////////////////////////////////////////

Utility functions and classes to facilitate the transfer of data from GestureWorks through
the bindings.

"""

from ctypes import POINTER, c_char_p, c_int, c_float, c_long, Structure
from math import sqrt, cos, sin, atan2

(TOUCHUPDATE, TOUCHADDED, TOUCHREMOVED) = (0, 1, 2)

"""Convert a GW mapstruct into a dictionary

Returns a dict mapping string names to float values

"""
def _mapStructToDict(mapstruct):
    assert isinstance(mapstruct, _MapStruct)
    names = []
    values = []
    for i in range(0, mapstruct.size):
        names.append(mapstruct.names[i])
        values.append(mapstruct.values[i])
    
    return dict(zip(names, values))

"""Simple point structure """
class Point(Structure):
    _fields_ = [('x', c_float),
                ('y', c_float),
                ('z', c_float),
                ('w', c_float),
                ('h', c_float),
                ('r', c_float)]

"""More useful point event structure

This is given by GestureWorks in a point event array

"""
class PointEvent(Structure):
    _fields_ = [('point_id', c_int), 
                ('status', c_int),
                ('position', Point),
                ('timestamp', c_long)]

"""Point event arrays are given by gestureworks when we consume point events

This is converted to a list of PointEvents in the bindings

"""
class _PointEventArray(Structure):
    _fields_ = [
                ('events', POINTER(PointEvent)),
                ('size', c_int),
                ]

"""GestureWorks structure

This is converted to a dict in the bindings

""" 
class _MapStruct(Structure):
    _fields_ = [
                ('names', POINTER(c_char_p)),
                ('values', POINTER(c_float)),
                ('size', c_int),
                ]

class _IntermediateGestureEvent(Structure):
    _fields_ = [
                ('ID', c_int),
                ('gesture_type', c_char_p),
                ('gesture_id', c_char_p),
                ('target', c_char_p),
                ('source', c_int),
                ('n', c_int),
                ('hold_n', c_int),
                ('x', c_float),
                ('y', c_float),
                ('timestamp', c_int),
                ('phase', c_int),
                ('locked_points', POINTER(c_int)),
                
                ('values', _MapStruct),
                ]

class _GestureEventArray(Structure):
    _fields_ = [
                ('size', c_int),
                ('events', POINTER(_IntermediateGestureEvent)),
                ]
        
"""The GestureEvent is returned by the bindings when we consume gesture events"""
class GestureEvent:
    def __init__(self, e):
        assert isinstance(e, _IntermediateGestureEvent)
        self.id = e.ID
        self.gesture_id = e.gesture_id
        self.target = e.target
        self.n = e.n
        self.x = e.x
        self.y = e.y
        self.timestamp = e.timestamp
        self.locked_points = []
        
        self.values = _mapStructToDict(e.values)
        
        if self.values.has_key('hold_n'):
            for i in range(0, self.dimension_values['hold_n']):
                self.locked_points.append(e.locked_points[i])
        
"""Rotate a 2D point around another point by a specified angle

Returns a tuple containing the transformed x and y coordinates of the point

"""
def rotateAboutCenter(point_x, point_y, center_x, center_y, ref_angle):
    local_x = point_x - center_x
    local_y = point_y - center_y
    
    length = sqrt(local_x*local_x + local_y*local_y)
    
    x = length * cos(ref_angle + atan2(local_y, local_x)) + center_x
    y = length * sin(ref_angle + atan2(local_y, local_x)) + center_y
    return (x, y)