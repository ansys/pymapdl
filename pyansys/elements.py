"""
Available as of 20.2:
LINK1
PLANE2
BEAM3
BEAM4
SOLID5
COMBIN7
LINK8
INFIN9
LINK10
LINK11
CONTAC12
PLANE13
COMBIN14
FLUID15
PIPE16
PIPE17
PIPE18
SURF19
PIPE20
MASS21
SURF22
BEAM23
BEAM24
PLANE25
MATRIX27
SHELL28
FLUID29
FLUID30
LINK31
LINK32
LINK33
LINK34
PLANE35
SOURC36
COMBIN37
FLUID38
COMBIN39
COMBIN40
SHELL41
PLANE42
SHELL43
BEAM44
SOLID45
SOLID46
INFIN47
MATRIX50
SHELL51
CONTAC52
PLANE53
BEAM54
PLANE55
SHELL57
PIPE59
PIPE60
SHELL61
SOLID62
SHELL63
SOLID64
SOLID65
FLUID66
PLANE67
LINK68
SOLID69
SOLID70
MASS71
PLANE75
PLANE77
PLANE78
FLUID79
FLUID80
FLUID81
PLANE82
PLANE83
SOLID87
VISCO88
VISCO89
SOLID90
SHELL91
SOLID92
SHELL93
CIRCU94
SOLID95
SOLID96
SOLID97
SOLID98
SHELL99
USER100
USER101
USER102
USER103
USER104
USER105
VISCO106
VISCO107
VISCO108
TRANS109
INFIN110
INFIN111
ROT112
INTER115
FLUID116
EDGE117
HF118
HF119
HF120
PLANE121
SOLID122
SOLID123
CIRCU124
CIRCU125
TRANS126
FLUID129
FLUID130
SHELL131
SHELL132
TRANS135
FLUID136
FLUID137
FLUID138
FLUID139
ROM140
SHELL143
ROM144
SURF151
SURF152
SURF153
SURF154
SURF155
SURF156
SHELL157
SURF159
TARGE169
TARGE170
CONTA171
CONTA172
CONTA173
CONTA174
CONTA175
CONTA176
CONTA177
CONTA178
PRETS179
LINK180
SHELL181
PLANE182
PLANE183
RBAR184
SOLID185
SOLID186
SOLID187
BEAM188
BEAM189
SOLID190
SOLID191
INTER192
INTER193
INTER194
INTER195
LAYER196
LAYER197
FOLLW201
INTER202
INTER203
INTER204
INTER205
INTER206
SHELL208
SHELL209
CPT212
CPT213
COMBI214
CPT215
CPT216
CPT217
FLUID218
FLUID219
FLUID220
FLUID221
PLANE222
SOLID223
SOLID225
SOLID226
SOLID227
PLANE230
SOLID231
SOLID232
PLANE233
SOLID236
SOLID237
PLANE238
SOLID239
SOLID240
HSFLD241
HSFLD242
COMBI250
SURF251
SURF252
INFIN257
INFIN258
INFIN259
INFIN260
GLINK262
REINF263
REINF264
REINF265
SOLID272
SOLID273
SOLID278
SOLID279
CABLE280
SHELL281
SHELL282
SHELL283
SOLID285
PIPE288
PIPE289
ELBOW290
SOLID291
PLANE292
PLANE293
USER300
"""
import numpy as np

# element type to VTK conversion function call map
# 0: skip
# 1: Point
# 2: Line (linear or quadratic)
# 3: Shell
# 4: 3D Solid (Hexahedral, wedge, pyramid, tetrahedral)
# 5: Tetrahedral
# 6: Line (always linear)

_etype_map = [0, 2,  # LINK1
	      3,  # PLANE2
	      3,  # BEAM3
	      2,  # BEAM4
	      4,  # SOLID5
	      0,  # UNUSED6
	      1,  # COMBIN7
	      2,  # LINK8
	      0,  # INFIN9
	      2,  # LINK10
	      2,  # LINK11
	      2,  # CONTAC12
	      3,  # PLANE13
	      2,  # COMBIN14
	      0,  # FLUID15
	      2,  # PIPE16
	      2,  # PIPE17
	      2,  # PIPE18
	      0,  # SURF19
	      2,  # PIPE20
	      1,  # MASS21
	      3,  # SURF22
	      2,  # BEAM23
	      2,  # BEAM24
	      3,  # PLANE25
	      0,  # UNUSED26
	      0,  # MATRIX27
	      3,  # SHELL28
	      3,  # FLUID29
	      4,  # FLUID30
	      2,  # LINK31
	      2,  # LINK32
	      2,  # LINK33
	      2,  # LINK34
	      3,  # PLANE35
	      0,  # SOURC36
	      2,  # COMBIN37
	      2,  # FLUID38
	      2,  # COMBIN39
	      2,  # COMBIN40
	      3,  # SHELL41
	      3,  # PLANE42
	      3,  # SHELL43
	      2,  # BEAM44
	      4,  # SOLID45
	      4,  # SOLID46
	      0,  # INFIN47
	      0,  # UNUSED48
	      0,  # UNUSED49
	      0,  # MATRIX50
	      3,  # SHELL51
	      0,  # CONTAC52
	      3,  # PLANE53
	      3,  # BEAM54
	      3,  # PLANE55
	      0,  # UNUSED56
	      3,  # SHELL57
	      0,  # UNUSED58
	      2,  # PIPE59
	      2,  # PIPE60
	      2,  # SHELL61
	      4,  # SOLID62
	      3,  # SHELL63
	      4,  # SOLID64
	      4,  # SOLID65
	      2,  # FLUID66
	      3,  # PLANE67
	      2,  # LINK68
	      4,  # SOLID69
	      4,  # SOLID70
	      1,  # MASS71
	      0,  # UNUSED72
	      0,  # UNUSED73
	      0,  # UNUSED74
	      3,  # PLANE75
	      0,  # UNUSED76
	      3,  # PLANE77
	      3,  # PLANE78
	      3,  # FLUID79
	      4,  # FLUID80
	      3,  # FLUID81
	      3,  # PLANE82
	      3,  # PLANE83
	      0,  # UNUSED84
	      0,  # UNUSED85
	      0,  # UNUSED86
	      5,  # SOLID87
	      3,  # VISCO88
	      4,  # VISCO89
	      4,  # SOLID90
	      3,  # SHELL91
	      5,  # SOLID92
	      3,  # SHELL93
	      0,  # CIRCU94
	      4,  # SOLID95
	      4,  # SOLID96
	      4,  # SOLID97
	      5,  # SOLID98
	      3,  # SHELL99
	      4,  # USER100
	      4,  # USER101
	      4,  # USER102
	      4,  # USER103
	      4,  # USER104
	      4,  # USER105
	      3,  # VISCO106
	      4,  # VISCO107
	      4,  # VISCO108
	      0,  # TRANS109
	      0,  # INFIN110
	      0,  # INFIN111
	      0,  # ROT112
	      0,  # UNUSED113
	      0,  # UNUSED114
	      3,  # INTER115
	      3,  # FLUID116
	      4,  # EDGE117
	      3,  # HF118
	      5,  # HF119
	      4,  # HF120
	      3,  # PLANE121
	      4,  # SOLID122
	      5,  # SOLID123
	      0,  # CIRCU124
	      0,  # CIRCU125
	      2,  # TRANS126
	      0,  # UNUSED127
	      0,  # UNUSED128
	      2,  # FLUID129
	      3,  # FLUID130
	      3,  # SHELL131
	      3,  # SHELL132
	      0,  # UNUSED133
	      0,  # UNUSED134
	      0,  # TRANS135
	      3,  # FLUID136
	      0,  # FLUID137
	      0,  # FLUID138
	      0,  # FLUID139
	      5,  # ROM140
	      0,  # UNUSED141
	      0,  # UNUSED142
	      3,  # SHELL143
	      0,  # ROM144
	      0,  # UNUSED145
	      0,  # UNUSED146
	      0,  # UNUSED147
	      0,  # UNUSED148
	      0,  # UNUSED149
	      0,  # UNUSED150
	      2,  # SURF151
	      3,  # SURF152
	      2,  # SURF153
	      3,  # SURF154
	      3,  # SURF155
	      2,  # SURF156
	      3,  # SHELL157
	      0,  # UNUSED158
	      0,  # SURF159
	      0,  # UNUSED160
	      2,  # BEAM161
	      0,  # UNUSED162
	      3,  # SHELL163
	      4,  # SOLID164
	      0,  # UNUSED165
	      0,  # UNUSED166
	      0,  # UNUSED167
	      5,  # SOLID168
	      0,  # TARGE169
	      0,  # TARGE170
	      2,  # CONTA171
	      2,  # CONTA172
	      3,  # CONTA173
	      3,  # CONTA174
	      1,  # CONTA175
	      2,  # CONTA176
	      2,  # CONTA177
	      2,  # CONTA178
	      0,  # PRETS179
	      2,  # LINK180
	      3,  # SHELL181
	      3,  # PLANE182
	      3,  # PLANE183
	      0,  # RBAR184
	      4,  # SOLID185
	      4,  # SOLID186
	      5,  # SOLID187
	      6,  # BEAM188
	      2,  # BEAM189
	      4,  # SOLSH190
              0,  # UNUSED191
	      4,  # INTER192
	      0,  # INTER193
	      0,  # INTER194
	      0,  # INTER195
	      0,  # LAYER196
	      0,  # LAYER197
	      0,  # UNUSED198
	      0,  # UNUSED199
	      0,  # UNUSED200
	      0,  # FOLLW201
	      0,  # INTER202
	      0,  # INTER203
	      0,  # INTER204
	      0,  # INTER205
	      0,  # INTER206
	      0,  # UNUSED207
	      2,  # SHELL208
	      2,  # SHELL209
	      0,  # UNUSED210
	      0,  # UNUSED211
	      0,  # CPT212
	      0,  # CPT213
	      0,  # COMBI214
	      0,  # CPT215
              0,  # UNUSED216
	      5,  # CPT217
	      3,  # FLUID218
	      3,  # FLUID219
	      4,  # FLUID220
	      5,  # FLUID221
	      3,  # PLANE222
	      3,  # PLANE223
	      0,  # UNUSED224
	      0,  # SOLID225
	      4,  # SOLID226
	      5,  # SOLID227
	      0,  # UNUSED228
	      0,  # UNUSED229
	      3,  # PLANE230
	      4,  # SOLID231
	      5,  # SOLID232
	      3,  # PLANE233
	      0,  # UNUSED234
	      0,  # UNUSED235
	      4,  # SOLID236
	      5,  # SOLID237
	      3,  # PLANE238
	      4,  # SOLID239
	      5,  # SOLID240
	      0,  # HSFLD241
	      0,  # HSFLD242
	      0,  # UNUSED243
	      0,  # UNUSED244
	      0,  # UNUSED245
	      0,  # UNUSED246
	      0,  # UNUSED247
	      0,  # UNUSED248
	      0,  # UNUSED249
	      2,  # COMBI250
	      2,  # SURF251
	      3,  # SURF252
	      0,  # UNUSED253
	      0,  # UNUSED254
	      0,  # UNUSED255
	      0,  # UNUSED256
	      0,  # INFIN257
	      0,  # INFIN258
	      0,  # INFIN259
              0,  # UNUSED260
	      4,  # UNUSED261
	      0,  # GLINK262
	      0,  # REINF263
	      0,  # REINF264
	      0,  # REINF265
	      0,  # UNUSED266
	      0,  # UNUSED267
	      0,  # UNUSED268
	      0,  # UNUSED269
	      0,  # UNUSED270
	      0,  # UNUSED271
	      0,  # SOLID272
	      0,  # SOLID273
	      0,  # UNUSED274
	      0,  # UNUSED275
	      0,  # UNUSED276
	      0,  # UNUSED277
	      4,  # SOLID278
	      4,  # SOLID279
	      2,  # CABLE280
	      3,  # SHELL281
	      3,  # SHELL282
	      3,  # SHELL283
	      0,  # UNUSED284
	      5,  # SOLID285
	      0,  # UNUSED286
	      0,  # UNUSED287
	      2,  # PIPE288
	      2,  # PIPE289
	      2,  # ELBOW290
	      5,  # SOLID291
	      3,  # PLANE292
	      3,  # PLANE293
	      0,  # UNUSED294
	      0,  # UNUSED295
	      0,  # UNUSED296
	      0,  # UNUSED297
	      0,  # UNUSED298
	      0,  # UNUSED299
	      0,  # USER300
]

ETYPE_MAP = np.array(_etype_map, dtype=np.int32)

