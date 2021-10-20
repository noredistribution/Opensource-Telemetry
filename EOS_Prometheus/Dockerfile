FROM centos:7 AS stage1
RUN yum install git rpm-build zip which -y
ENV HOME /workdir
WORKDIR /workdir
RUN mkdir -p /workdir/download
RUN curl -L -o /workdir/download/go.tar.gz https://dl.google.com/go/go1.14.3.linux-amd64.tar.gz
RUN tar xfz /workdir/download/go.tar.gz --directory /workdir/download/
RUN mkdir -p /workdir/build/goarista
RUN git clone https://github.com/aristanetworks/goarista.git /workdir/build/goarista
ENV GOROOT /workdir/download/go
ENV GOPATH /workdir/build/go
RUN git clone https://github.com/jordansissel/fpm.git /workdir/build/fpm
ENV PATH="${PATH}:${GOROOT}/bin"
ENV PATH="${PATH}:/workdir/.rbenv/bin:/workdir/.rbenv/shims"
# RUN yum install ruby-devel gcc make rpm-build rubygems -y
RUN yum install git-core zlib zlib-devel gcc-c++ patch readline readline-devel libyaml-devel libffi-devel openssl-devel make bzip2 autoconf automake libtool bison curl sqlite-devel -y
RUN curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash -
RUN echo 'eval "$(rbenv init -)"' >> ~/.bashrc
RUN source ~/.bashrc
RUN rbenv install 2.7.1
RUN rbenv global 2.7.1
RUN gem install --no-document fpm
RUN mkdir -p /workdir/build/go/src
RUN ln -s /workdir/build/goarista/cmd/ocprometheus /workdir/build/go/src
RUN cd $GOPATH/src/ocprometheus && go get
RUN cd /workdir/build/goarista/cmd/ocprometheus && GOOS=linux GOARCH=386 go build
RUN cp /workdir/build/goarista/cmd/ocprometheus/ocprometheus /workdir
RUN cd /workdir && fpm -s dir -t rpm -a all -n "ocprometheus-i386" -v1.9.6  --prefix /usr/bin/ -C /workdir ocprometheus
RUN cd /workdir && echo 'format: 1' >> /workdir/manifest.txt
RUN echo 'primaryRpm: ocprometheus-i386-1.9.6-1.noarch.rpm' >> /workdir/manifest.txt
RUN GITLASTCOMDATE=$(cd /workdir/build/goarista/ && sh -c "git log -1 --date=short --format=%cd | sed 's/-//g'") \
  GITLASTCOMMIT=$(cd /workdir/build/goarista/ && sh -c "git rev-parse --short HEAD") \
  SHA1SUM=$(cd /workdir/ && sha1sum ocprometheus-i386-1.9.6-1.noarch.rpm | cut -d ' ' -f 1) \
  && cd /workdir/ && echo 'ocprometheus-i386-1.9.6-1.noarch.rpm-sha1: $(SHA1SUM)' >> /workdir/manifest.txt \
  && zip ocprometheus-${GITLASTCOMDATE}-${GITLASTCOMMIT}-i386.zip manifest.txt ocprometheus-i386-1.9.6-1.noarch.rpm \
  &&  cd /workdir/ && cp "ocprometheus-${GITLASTCOMDATE}-${GITLASTCOMMIT}-i386.zip" ocprometheus-${GITLASTCOMDATE}-${GITLASTCOMMIT}-i386.swix
FROM scratch AS export-stage
COPY --from=stage1 /workdir/ocprometheus*.swix .

