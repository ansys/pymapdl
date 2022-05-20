# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import sys
import time

from opentelemetry import _metrics
from opentelemetry.exporter.otlp.proto.grpc._metric_exporter import (
    OTLPMetricExporter
)

from opentelemetry.sdk._metrics import MeterProvider
from opentelemetry.sdk._metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)

class Metric:
    def __init__(self, otlp_endpoint, name, version):
        # If no OTEL exporter is specified, fallback to console
        # Should be revamped to handle silent as well, ...
        exporter = (OTLPMetricExporter(endpoint=otlp_endpoint,
                                       insecure=True)
                    if otlp_endpoint is not None
                    else ConsoleMetricExporter())

        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=15000, export_timeout_millis=10000)
        provider = MeterProvider(metric_readers=[reader])

        _metrics.set_meter_provider(provider)
        self._meter = provider.get_meter(name, version)
        self.counter = self._meter.create_counter(name="nb_calls", description="Number of call to the API.")

    def increment_counter(self):
        self.counter.add(1)

    def get_meter(self):
        return self._meter

    def set_meter(self, value):
        self._meter = value

    meter = property(get_meter, set_meter)