pipelineJob("ci-linchpin-messageBus-trigger") {
    definition {
        logRotator {
            numToKeep(100)
        }

        concurrentBuild(false)

        parameters {
            stringParam(
                    "CI_MESSAGE",
                    "",
                    "fedmsg msg"
            )
        }

        triggers {
            ciBuildTrigger {
                providerData {
                    fedMsgSubscriberProviderData {
                        name('fedora-fedmsg')
                        overrides {
                            topic('org.centos.prod.ci.linchpin.pr.queued')
                        }
                    }
                }
                noSquash(true)
            }
        }

        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/CentOS-PaaS-SIG/linchpin')
                        refspec("+refs/heads/*:refs/remotes/origin/* +refs/pull/*:refs/remotes/origin/pr/*")
                    }
                    branch('develop')
                }
            }
            scriptPath("config/Dockerfiles/JenkinsfileMessageBusTrigger")
            lightweight(false)
        }
    }
}
