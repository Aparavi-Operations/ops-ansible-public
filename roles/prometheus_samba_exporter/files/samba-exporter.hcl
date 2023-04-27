service {
  name = "samba-exporter"
  tags = ["prometheus-exporter"]
  port = 9922

  check {
    id                       = "samba-exporter"
    name                     = "Samba exxporter healthcheck"
    http                     = "http://localhost:9922"
    method                   = "GET"
    interval                 = "15s"
    timeout                  = "2s"
    success_before_passing   = 2
    failures_before_warning  = 1
    failures_before_critical = 2
  }
}
