# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Markus Weber
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from http import HTTPStatus
from typing import List, Dict
from uuid import UUID

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from uim.codec.parser.uim import UIMParser
from uim.codec.writer.encoder.encoder_3_1_0 import UIMEncoder310
from uim.model.base import InkModelException
from uim.model.ink import InkModel
# Mime-type for Universal Ink Model
from uim.model.inkinput.inputdata import InputContext, SensorContext, InkInputProvider, InkInputType
from uim.model.inkinput.sensordata import SensorData

VND_WACOM_INK_MODEL: str = 'application/vnd.wacom-ink.model'

description: str = """
Simple backend for processing of Universal Ink Model (UIM) files.
"""


# FastAPI for
app: FastAPI = FastAPI(
    title="UIM demo backend.",
    description=description,
    version="0.0.1",
    terms_of_service="",
    contact={
        "name": "Markus Weber",
        "url": "https://github.com/doctorink/",
        "email": "Markus.Weber@wacom.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://choosealicense.com/licenses/mit/",
    },
)

origins: List[str] = ["*"]

# Configure the CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process")
def uim(uim_file: UploadFile = File(...)):
    if uim_file is None or uim_file.file is None:
        raise HTTPException(status_code=400, detail="Please provide a Universal Ink Model when calling this request")
    content: bytes = uim_file.file.read()
    uim_parser: UIMParser = UIMParser()
    try:
        ink_model: InkModel = uim_parser.parse(content)
        # Perform your network classification here
        # ...
    except InkModelException as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=f"No valid UIM content. Exception:= {e}")
    encoder: UIMEncoder310 = UIMEncoder310()
    return Response(content=encoder.encode(ink_model), media_type=VND_WACOM_INK_MODEL)


@app.post("/input-provider-coloring")
def color_coding(uim_file: UploadFile = File(...)):
    if uim_file is None or uim_file.file is None:
        raise HTTPException(status_code=400, detail="Please provide a Universal Ink Model when calling this request")
    content: bytes = uim_file.file.read()
    uim_parser: UIMParser = UIMParser()
    try:
        ink_model: InkModel = uim_parser.parse(content)
        input_provider_map: Dict[UUID, InkInputProvider] = dict([(iip.id, iip) for iip in
                                                                 ink_model.input_configuration.ink_input_providers])
        # Iterate over strokes
        for stroke in ink_model.strokes:

            # Stroke is produced by sensor data being processed by the ink geometry pipeline
            sd: SensorData = ink_model.sensor_data.sensor_data_by_id(stroke.sensor_data_id)
            # Get InputContext for the sensor data
            input_context: InputContext = ink_model.input_configuration.get_input_context(sd.input_context_id)
            # Retrieve SensorContext
            sensor_context: SensorContext = ink_model.input_configuration \
                .get_sensor_context(input_context.sensor_context_id)
            for scc in sensor_context.sensor_channels_contexts:
                # Sensor channel context is referencing input device
                ink_input_provider: InkInputProvider = input_provider_map[scc.input_provider_id]

                # depending on the input  provider we simple color code the model
                if ink_input_provider.type == InkInputType.MOUSE:
                    stroke.style.path_point_properties.red = 1.
                    stroke.style.path_point_properties.green = 0.
                    stroke.style.path_point_properties.blue = 0.
                elif ink_input_provider.type == InkInputType.PEN:
                    stroke.style.path_point_properties.red = 0.
                    stroke.style.path_point_properties.green = 1.
                    stroke.style.path_point_properties.blue = 0.
                elif ink_input_provider.type == InkInputType.TOUCH:
                    stroke.style.path_point_properties.red = 0.
                    stroke.style.path_point_properties.green = 0.
                    stroke.style.path_point_properties.blue = 1.

    except InkModelException as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=f"No valid UIM content. Exception:= {e}")
    encoder: UIMEncoder310 = UIMEncoder310()
    return Response(content=encoder.encode(ink_model), media_type=VND_WACOM_INK_MODEL)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, access_log=True)
