{{- define "confida-integra.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "confida-integra.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "confida-integra.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "confida-integra.labels" -}}
app.kubernetes.io/name: {{ include "confida-integra.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version }}
{{- end -}}

{{- define "confida-integra.selectorLabels" -}}
app.kubernetes.io/name: {{ include "confida-integra.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
