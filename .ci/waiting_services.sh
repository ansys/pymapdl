#!/bin/bash
echo "::group:: Docker services" && docker ps && echo "::endgroup::"

echo "Waiting for the MAPDL service to be up..."
nc -v -z localhost "$PYMAPDL_PORT"

echo "::group:: ps aux Output" && ps aux && echo "::endgroup::"


echo "::group:: Waiting for the MAPDL port to be open..."
while ! nc -z localhost "$PYMAPDL_PORT"; do
    sleep 0.1
done
echo "::endgroup::"
echo "MAPDL service is up!"


echo "::group:: Waiting for the DPF port to be open..."
if [ "$TEST_DPF_BACKEND" = "true" ]; then
    while ! nc -z localhost "$DPF_PORT"; do
        sleep 0.1
    done
    echo "DPF service is up!"
else
    echo "TEST_DPF_BACKEND is not set to true, skipping DPF service check."
fi
echo "::endgroup::"
