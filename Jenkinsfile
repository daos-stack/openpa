#!/usr/bin/groovy
/* Copyright (C) 2019 Intel Corporation
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted for any purpose (including commercial purposes)
 * provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions, and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions, and the following disclaimer in the
 *    documentation and/or materials provided with the distribution.
 *
 * 3. In addition, redistributions of modified forms of the source or binary
 *    code must carry prominent notices stating that the original code was
 *    changed and the date of the change.
 *
 *  4. All publications or advertising materials mentioning features or use of
 *     this software are asked, but not required, to acknowledge that it was
 *     developed by Intel Corporation and credit the contributors.
 *
 * 5. Neither the name of Intel Corporation, nor the name of any Contributor
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
// To use a test branch (i.e. PR) until it lands to master
// I.e. for testing library changes
//@Library(value="pipeline-lib@your_branch") _

pipeline {
    agent none

    stages {
        stage('Cancel Previous Builds') {
            when { changeRequest() }
            steps {
                cancelPreviousBuilds()
            }
        }
        stage('Lint') {
            stages {
                stage('RPM Lint') {
                    agent {
                        dockerfile {
                            filename 'Dockerfile.centos.7'
                            label 'docker_runner'
                            additionalBuildArgs  '--build-arg UID=$(id -u)'
                            args  '--group-add mock --cap-add=SYS_ADMIN --privileged=true'
                        }
                    }
                    steps {
                        sh 'make rpmlint'
                    }
                }
            }
        }
        stage('Build') {
            parallel {
                stage('Build on CentOS 7') {
                    agent {
                        dockerfile {
                            filename 'Dockerfile.centos.7'
                            label 'docker_runner'
                            additionalBuildArgs '--build-arg UID=$(id -u) --build-arg JENKINS_URL=' +
                                                env.JENKINS_URL
                            args  '--group-add mock --cap-add=SYS_ADMIN --privileged=true'
                        }
                    }
                    steps {
                        sh '''rm -rf artifacts/centos7/
                              mkdir -p artifacts/centos7/
                              make srpm
                              make mockbuild'''
                    }
                    post {
                        success {
                             sh '''(cd /var/lib/mock/epel-7-x86_64/result/ &&
                                    cp -r . $OLDPWD/artifacts/centos7/)
                                   createrepo artifacts/centos7/'''
                            archiveArtifacts artifacts: 'artifacts/centos7/**'
                        }
                        failure {
                            sh '''cp -af _topdir/SRPMS artifacts/centos7/
                                  (cd /var/lib/mock/epel-7-x86_64/result/ &&
                                   cp -r . $OLDPWD/artifacts/centos7/)
                                  (cd /var/lib/mock/epel-7-x86_64/root/builddir/build/BUILD/*/
                                   find . -name configure -printf %h\\\\n | \
                                   while read dir; do
                                       if [ ! -f $dir/config.log ]; then
                                           continue
                                       fi
                                       tdir="$OLDPWD/artifacts/centos7/autoconf-logs/$dir"
                                       mkdir -p $tdir
                                       cp -a $dir/config.log $tdir/
                                   done)'''
                            archiveArtifacts artifacts: 'artifacts/centos7/**'
                        }
                    }
                }
                stage('Build on Leap 15') {
                    agent {
                        dockerfile {
                            filename 'Dockerfile.leap.15'
                            label 'docker_runner'
                            additionalBuildArgs '--build-arg UID=$(id -u) --build-arg JENKINS_URL=' +
                                                env.JENKINS_URL
                            args  '--privileged=true'
                        }
                    }
                    steps {
                        sh '''rm -rf artifacts/leap15.1/
                              mkdir -p artifacts/leap15.1/
                              make srpm
                              ls -l /dev/fd || true
                              ls -l /proc/self/fd || true
                              sudo build --repo http://download.opensuse.org/distribution/leap/15.1/repo/oss/ \
                                         --dist sl15.1 openpa.spec'''
                    }
                    post {
                        success {
                            sh '''(cd /var/tmp/build-root/home/abuild/rpmbuild/ &&
                                   cp {RPMS/*,SRPMS}/* $OLDPWD/artifacts/leap15.1/)
                                  createrepo artifacts/leap15.1/'''
                            archiveArtifacts artifacts: 'artifacts/leap15.1/**'
                        }
                        failure {
                            sh '''(cd /var/tmp/build-root/home/abuild/rpmbuild/BUILD &&
                                   find . -name configure -printf %h\\\\n | \
                                   while read dir; do
                                       if [ ! -f $dir/config.log ]; then
                                           continue
                                       fi
                                       tdir="$OLDPWD/artifacts/leap15.1/autoconf-logs/$dir"
                                       mkdir -p $tdir
                                       cp -a $dir/config.log $tdir/
                                   done)'''
                            archiveArtifacts artifacts: 'artifacts/leap15.1/**'
                        }
                    }
                }
                stage('Build on SLES 12.3') {
                    when { beforeAgent true
                           environment name: 'SLES12_3_DOCKER', value: 'true' }
                    agent {
                        dockerfile {
                            filename 'Dockerfile.sles.12.3'
                            label 'docker_runner'
                            additionalBuildArgs '--build-arg UID=$(id -u) --build-arg JENKINS_URL=' +
                                                env.JENKINS_URL
                            args  '--privileged=true'
                        }
                    }
                    steps {
                        sh '''rm -rf artifacts/sles12.3/
                              mkdir -p artifacts/sles12.3/
                              make srpm
                              sudo build --repo http://cobbler.wolf.hpdd.intel.com/cobbler/ks_mirror/SLES-12.3-x86_64/ \
                                         --dist sle12.3 openpa.spec'''
                    }
                    post {
                        success {
                            sh '''(cd /var/tmp/build-root/home/abuild/rpmbuild/ &&
                                   cp {RPMS/*,SRPMS}/* $OLDPWD/artifacts/sles12.3/)
                                  createrepo artifacts/sles12.3/'''
                            archiveArtifacts artifacts: 'artifacts/sles12.3/**'
                        }
                        failure {
                            sh '''(cd /var/tmp/build-root/home/abuild/rpmbuild/BUILD &&
                                   find . -name configure -printf %h\\\\n | \
                                   while read dir; do
                                       if [ ! -f $dir/config.log ]; then
                                           continue
                                       fi
                                       tdir="$OLDPWD/artifacts/sles12.3/autoconf-logs/$dir"
                                       mkdir -p $tdir
                                       cp -a $dir/config.log $tdir/
                                   done)'''
                            archiveArtifacts artifacts: 'artifacts/sles12.3/**'
                        }
                    }
                }
                stage('Build on Leap 42.3') {
                    agent {
                        dockerfile {
                            filename 'Dockerfile.leap.42.3'
                            label 'docker_runner'
                            additionalBuildArgs  '--build-arg UID=$(id -u) ' +
                                                 "--build-arg CACHEBUST=${currentBuild.startTimeInMillis}"
                        }
                    }
                    steps {
                        sh '''rm -rf artifacts/leap42.3/
                              mkdir -p artifacts/leap42.3/
                              make srpm
                              id
                              sudo id
                              ls -l /dev/fd || true
                              ls -l /proc/self/fd || true
                              sudo build --repo http://download.opensuse.org/distribution/leap/42.3/repo/oss/suse \
                                         --dist sl42.3 openpa.spec'''
                    }
                    post {
                        success {
                            sh '''(cd /var/tmp/build-root/home/abuild/rpmbuild/ &&
                                   cp {RPMS/*,SRPMS}/* $OLDPWD/artifacts/leap42.3/)
                                  createrepo artifacts/leap42.3/'''
                            archiveArtifacts artifacts: 'artifacts/leap42.3/**'
                        }
                        failure {
                            sh '''(cd /var/tmp/build-root/home/abuild/rpmbuild/BUILD &&
                                   find . -name configure -printf %h\\\\n | \
                                   while read dir; do
                                       if [ ! -f $dir/config.log ]; then
                                           continue
                                       fi
                                       tdir="$OLDPWD/artifacts/leap42.3/autoconf-logs/$dir"
                                       mkdir -p $tdir
                                       cp -a $dir/config.log $tdir/
                                   done)'''
                            archiveArtifacts artifacts: 'artifacts/leap42.3/**'
                        }
                    }
                }
                // This stage will not be needed once Cart is updated
                // to a newer scons_local
                stage('Build on Ubuntu 18.04') {
                    agent {
                        dockerfile {
                            filename 'Dockerfile.ubuntu.18.04'
                            label 'docker_runner'
                            additionalBuildArgs  '--build-arg UID=$(id -u) ' +
                                                 "--build-arg CACHEBUST=${currentBuild.startTimeInMillis}"
                        }
                    }
                    steps {
                        sh '''rm -rf artifacts/ubuntu18.04/
                              mkdir -p artifacts/ubuntu18.04/
                              : "${DEBEMAIL:="$env.DAOS_EMAIL"}"
                              : "${DEBFULLNAME:="$env.DAOS_FULLNAME"}"
                              export DEBEMAIL
                              export DEBFULLNAME
                              make debs'''
                    }
                    post {
                        success {
                            sh '''ln -v \
                                   _topdir/BUILD/*{.build,.changes,.deb,.dsc,.gz,.xz} \
                                   artifacts/ubuntu18.04/
                                  pushd artifacts/ubuntu18.04/
                                    dpkg-scanpackages . /dev/null | \
                                      gzip -9c > Packages.gz
                                  popd'''
                            archiveArtifacts artifacts: 'artifacts/ubuntu18.04/**'
                        }
                        failure {
                            sh script: "cat _topdir/BUILD/*.build",
                               returnStatus: true
                            archiveArtifacts artifacts: 'artifacts/ubuntu18.04/**'
                        }
                    }
                }
            }
        }
    }
}
