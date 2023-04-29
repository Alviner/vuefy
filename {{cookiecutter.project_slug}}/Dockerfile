FROM snakepacker/python:all AS builder

RUN python3.11 -m venv /usr/share/python3/app
RUN /usr/share/python3/app/bin/pip install -U setuptools wheel

# bump this number for invalidating installing dependencies
# cache for following layers
ENV DOCKERFILE_VERSION 1

COPY dist/ /mnt/dist
RUN /usr/share/python3/app/bin/pip install -U /mnt/dist/*.whl

RUN find-libdeps /usr/share/python3/app > /usr/share/python3/app/pkgdeps.txt

########################################################################
FROM snakepacker/python:3.11 as release

COPY --from=builder /usr/share/python3/app /usr/share/python3/app
RUN xargs -ra /usr/share/python3/app/pkgdeps.txt apt-install
RUN find /usr/share/python3/app/bin/ -name '{{ cookiecutter.project_slug }}*' -exec ln -snf '{}' /usr/bin/ ';'

CMD ["{{ cookiecutter.project_slug }}_admin"]
