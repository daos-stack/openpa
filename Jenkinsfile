pipeline {
    agent none

    stages {
        stage('Lint') {
            stages {
                stage('RPM Lint') {
            agent {
                dockerfile {
                    filename 'Dockerfile.centos:7'
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
                            filename 'Dockerfile.centos:7'
                            label 'docker_runner'
                            additionalBuildArgs  '--build-arg UID=$(id -u)'
                            args  '--group-add mock --cap-add=SYS_ADMIN --privileged=true'
                        }
                    }
                    steps {
                        sh '''rm -rf artifacts/centos\\ 7/
                              mkdir -p artifacts/centos\\ 7/
                              if make srpm; then
                                  if make mockbuild; then
                                      (cd /var/lib/mock/epel-7-x86_64/result/ &&
                                       cp -r . $OLDPWD/artifacts/centos\\ 7/)
                                      createrepo artifacts/centos\\ 7/
                                  else
                                      rc=\${PIPESTATUS[0]}
                                      (cd /var/lib/mock/epel-7-x86_64/result/ &&
                                       cp -r . $OLDPWD/artifacts/centos\\ 7/)
                                      cp -af _topdir/SRPMS artifacts/centos\\ 7/
                                      exit \$rc
                                  fi
                              else
                                  exit \${PIPESTATUS[0]}
                              fi'''
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'artifacts/centos 7/**'
                        }
                    }
                }
                stage('Build on SLES 12.3') {
                    agent {
                        dockerfile {
                            filename 'Dockerfile.sles.12.3'
                            label 'docker_runner'
                            additionalBuildArgs  '--build-arg UID=$(id -u)'
                        }
                    }
                    steps {
                        sh '''rm -rf artifacts/sles\\ 12.3/
                              mkdir -p artifacts/sles\\ 12.3/
                              if make rpms; then
                                  cp -af _topdir/{S,}RPMS artifacts/sles\\ 12.3/
                                  createrepo artifacts/sles\\ 12.3/
                              else
                                  exit \${PIPESTATUS[0]}
                              fi'''
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'artifacts/sles 12.3/**'
                        }
                    }
                }
                stage('Build on Ubuntu 16.04') {
                    agent {
                        label 'docker_runner'
                    }
                    steps {
                        echo "Building on Ubuntu is not implemented for the moment"
                    }
                }
            }
        }
    }
}
