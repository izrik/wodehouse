#!/bin/sh

hashin -r requirements-lock.txt $( cat requirements.txt )
hashin -r dev-requirements-lock.txt $( cat dev-requirements.txt )
