# Articles

https://eos.arista.com/streaming-eos-telemetry-states-to-prometheus/


https://eos.arista.com/understanding-subscription-paths-for-open-source-telemetry-streaming/

## Automate swix generation

 Run:
`DOCKER_BUILDKIT=1 docker build -f Dockerfile -t eos-ocadapters --output out .`

This will generate the ocprometheus swix file in the `out` directory, which then can be SCPd to EOS and installed as an extension:

```
total 14464
-rw-r--r--  1 tamas  staff  7204182 Aug 13 21:04 ocprometheus-20200805-fd197cf-i386.swix
```

Tested on macOS Catalina and Centos 7.6.1810

First runs take about 10 minutes and subsequent runs should take a few seconds as things are cached already.

e.g.:

```
[root@master-node EOS_Prometheus]# DOCKER_BUILDKIT=1 docker build -f Dockerfile -t eos-ocadapters --output out .
[+] Building 539.1s (30/30) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                                 0.0s
 => => transferring dockerfile: 2.43kB                                                                                                                                               0.0s
 => [internal] load .dockerignore                                                                                                                                                    0.0s
 => => transferring context: 2B                                                                                                                                                      0.0s
 => [internal] load metadata for docker.io/library/centos:7                                                                                                                          1.8s
 => [stage1 1/25] FROM docker.io/library/centos:7@sha256:19a79828ca2e505eaee0ff38c2f3fd9901f4826737295157cc5212b7a372cd2b                                                           14.6s
 => => resolve docker.io/library/centos:7@sha256:19a79828ca2e505eaee0ff38c2f3fd9901f4826737295157cc5212b7a372cd2b                                                                    0.0s
 => => sha256:19a79828ca2e505eaee0ff38c2f3fd9901f4826737295157cc5212b7a372cd2b 1.20kB / 1.20kB                                                                                       0.0s
 => => sha256:fe2347002c630d5d61bf2f28f21246ad1c21cc6fd343e70b4cf1e5102f8711a9 529B / 529B                                                                                           0.0s
 => => sha256:7e6257c9f8d8d4cdff5e155f196d67150b871bbe8c02761026f803a704acb3e9 2.79kB / 2.79kB                                                                                       0.0s
 => => sha256:75f829a71a1c5277a7abf55495ac8d16759691d980bf1d931795e5eb68a294c0 75.86MB / 75.86MB                                                                                     2.5s
 => => extracting sha256:75f829a71a1c5277a7abf55495ac8d16759691d980bf1d931795e5eb68a294c0                                                                                           11.3s
 => [stage1 2/25] RUN yum install git rpm-build zip which -y                                                                                                                        29.0s
 => [stage1 3/25] WORKDIR /workdir                                                                                                                                                   0.0s
 => [stage1 4/25] RUN mkdir -p /workdir/download                                                                                                                                     0.6s
 => [stage1 5/25] RUN curl -L -o /workdir/download/go.tar.gz https://dl.google.com/go/go1.14.3.linux-amd64.tar.gz                                                                   10.6s
 => [stage1 6/25] RUN tar xfz /workdir/download/go.tar.gz --directory /workdir/download/                                                                                             6.3s
 => [stage1 7/25] RUN mkdir -p /workdir/build/goarista                                                                                                                               0.6s
 => [stage1 8/25] RUN git clone https://github.com/aristanetworks/goarista.git /workdir/build/goarista                                                                               3.9s
 => [stage1 9/25] RUN git clone https://github.com/jordansissel/fpm.git /workdir/build/fpm                                                                                           4.0s
 => [stage1 10/25] RUN yum install git-core zlib zlib-devel gcc-c++ patch readline readline-devel libyaml-devel libffi-devel openssl-devel make bzip2 autoconf automake libtool bi  31.3s
 => [stage1 11/25] RUN curl -sL https://github.com/rbenv/rbenv-installer/raw/master/bin/rbenv-installer | bash -                                                                    11.7s
 => [stage1 12/25] RUN echo 'eval "$(rbenv init -)"' >> ~/.bashrc                                                                                                                    0.6s
 => [stage1 13/25] RUN source ~/.bashrc                                                                                                                                              0.7s
 => [stage1 14/25] RUN rbenv install 2.7.1                                                                                                                                         257.2s
 => [stage1 15/25] RUN rbenv global 2.7.1                                                                                                                                            0.7s
 => [stage1 16/25] RUN gem install --no-document fpm                                                                                                                                18.1s
 => [stage1 17/25] RUN mkdir -p /workdir/build/go/src                                                                                                                                0.7s
 => [stage1 18/25] RUN ln -s /workdir/build/goarista/cmd/ocprometheus /workdir/build/go/src                                                                                          0.7s
 => [stage1 19/25] RUN cd /workdir/build/go/src/ocprometheus && go get                                                                                                             106.2s
 => [stage1 20/25] RUN cd /workdir/build/goarista/cmd/ocprometheus && GOOS=linux GOARCH=386 go build                                                                                29.3s
 => [stage1 21/25] RUN cp /workdir/build/goarista/cmd/ocprometheus/ocprometheus /workdir                                                                                             0.6s
 => [stage1 22/25] RUN cd /workdir && fpm -s dir -t rpm -a all -n "ocprometheus-i386" -v1.9.6  --prefix /usr/bin/ -C /workdir ocprometheus                                           4.7s
 => [stage1 23/25] RUN cd /workdir && echo 'format: 1' >> /workdir/manifest.txt                                                                                                      0.5s
 => [stage1 24/25] RUN echo 'primaryRpm: ocprometheus-i386-1.9.6-1.noarch.rpm' >> /workdir/manifest.txt                                                                              0.6s
 => [stage1 25/25] RUN GITLASTCOMDATE=$(cd /workdir/build/goarista/ && sh -c "git log -1 --date=short --format=%cd | sed 's/-//g'")   GITLASTCOMMIT=$(cd /workdir/build/goarista/ &  1.0s
 => [export-stage 1/1] COPY --from=stage1 /workdir/ocprometheus*.swix .                                                                                                              0.8s
 => exporting to client                                                                                                                                                              0.0s
 => => copying files 7.21MB                                                                                                                                                          0.0s
```
