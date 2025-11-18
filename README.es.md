# Enjambre de Agentes Codex

Codex Agents Swarm es un marco ligero que conecta el complemento OpenAI Codex con cualquier IDE donde esté instalado. Trata la sesión del IDE como un espacio de trabajo cooperativo multiagente, lo que te permite orquestar agentes especializados que colaboran en tareas que van desde desarrollo de software hasta documentación, planificación o investigación.

## Cómo funciona

1. **Contrato centrado en el orquestador.** `AGENTS.md` define únicamente las reglas globales, el estado compartido y el agente ORCHESTRATOR. El orquestador interpreta el objetivo del usuario, redacta un plan, solicita aprobación y delega el trabajo en otros agentes.
2. **Registro externo de agentes.** Cada agente que no es el orquestador vive en `.AGENTS/<ID>.json`. Cuando el IDE carga este repositorio, importa dinámicamente cada documento JSON y registra el ID del agente, su rol, permisos y flujo de trabajo.
3. **Estado compartido de tareas.** Los planes legibles para humanos viven en `PLAN.md`, mientras que el progreso legible por máquinas se mantiene en `.AGENTS/TASKS.json`. Esta separación permite que los agentes comuniquen actualizaciones de estado sin importar en qué IDE se ejecuten.
4. **Operación agnóstica del complemento.** Como las instrucciones son Markdown y JSON, cualquier IDE que admita el complemento Codex puede ejecutar los mismos flujos sin configuración adicional.

## Estructura del repositorio

```
.
├── AGENTS.md
├── LICENSE
├── PLAN.md
├── README.md
└── .AGENTS/
    ├── PLANNER.json
    ├── CODER.json
    ├── REVIEWER.json
    ├── DOCS.json
    ├── CREATOR.json
    └── TASKS.json
```

| Ruta | Propósito |
| --- | --- |
| `AGENTS.md` | Reglas globales, flujo de trabajo de commits y especificación del ORCHESTRATOR (incluida la plantilla JSON para nuevos agentes). |
| `.AGENTS/PLANNER.json` | Define cómo se agregan o actualizan tareas en `PLAN.md` y `.AGENTS/TASKS.json`. |
| `.AGENTS/CODER.json` | Especialista en implementación responsable de editar código o configuración ligados a IDs de tareas. |
| `.AGENTS/REVIEWER.json` | Realiza revisiones, verifica el trabajo y cambia el estado de las tareas en consecuencia. |
| `.AGENTS/DOCS.json` | Mantiene README y otros documentos sincronizados con el trabajo recién completado. |
| `.AGENTS/CREATOR.json` | Fábrica de agentes bajo demanda que escribe nuevos agentes JSON y actualiza el registro. |
| `.AGENTS/TASKS.json` | Espejo legible por máquinas del backlog; es la fuente canónica cuando aparecen discrepancias. |
| `PLAN.md` | Backlog legible para humanos compartido en la conversación (secciones Backlog / Done). |
| `README.md` | Descripción general y material de incorporación del repositorio. |
| `LICENSE` | Licencia MIT del proyecto. |

## Ciclo de vida del agente

1. **Planificación:** El ORCHESTRATOR lee `AGENTS.md`, carga `.AGENTS/*.json` y crea un plan que asigna cada paso a un agente registrado (por ejemplo, PLANNER, CODER, REVIEWER, DOCS).
2. **Aprobación:** El usuario puede aprobar, editar o cancelar el plan antes de que comience cualquier trabajo.
3. **Ejecución:** El orquestador cambia el `agent_mode` según el plan, permitiendo que cada agente siga su flujo de trabajo definido en JSON dentro del IDE.
4. **Seguimiento del progreso:** Los agentes actualizan `PLAN.md` y `.AGENTS/TASKS.json` según sus permisos, garantizando que tanto humanos como herramientas vean el estado actual.

Esta estructura permite encadenar flujos arbitrarios como implementación de código, actualización de documentación, resúmenes de investigación o triaje de tareas, todo desde la misma sesión del IDE.

## Flujo de trabajo de commits

- El espacio de trabajo siempre es un repositorio git, por lo que cada cambio significativo debe versionarse.
- Cada tarea atómica listada en `PLAN.md` se asigna exactamente a un commit con un mensaje conciso y fácil de leer (idealmente haciendo referencia al ID de la tarea).
- El agente que realiza el trabajo prepara y hace commit antes de devolver el control al orquestador, y el orquestador pausa el plan hasta que ese commit exista.
- Los resúmenes de cada paso mencionan el nuevo hash del commit y confirman que el árbol de trabajo está limpio para que las personas puedan auditar el progreso directamente desde la conversación.
- Si un paso del plan no produce cambios en archivos, indícalo explícitamente; de lo contrario, el enjambre no debe continuar sin un commit.

## Detalles del estado compartido

- **`PLAN.md`**: Lista Markdown con casillas de verificación pensada para humanos. Incluye tareas con IDs, secciones (Backlog, In Progress, Done) y estado. Los agentes siempre la leen por completo antes de editar y, cada vez que una tarea pasa a completada, agregan de inmediato una línea con sangría `Review:` que resuma (en una o dos oraciones) qué cambió y por qué.
- **`.AGENTS/TASKS.json`**: Espejo para máquinas con un esquema JSON estricto, de modo que los agentes puedan analizar, filtrar y actualizar el estado de forma determinista. Cuando ocurren discrepancias, `.AGENTS/TASKS.json` es la fuente canónica y `PLAN.md` debe reconciliarse.

## Cómo agregar un nuevo agente

1. Duplica la plantilla definida en `AGENTS.md` bajo “JSON Template for New Agents”.
2. Guarda el archivo como `.AGENTS/<AGENT_ID>.json` usando un ID en mayúsculas (por ejemplo, `RESEARCHER.json`).
3. Completa el `role`, `description`, `inputs`, `outputs`, `permissions` y la lista ordenada `workflow` que describe exactamente cómo debe comportarse el agente.
4. Haz commit del archivo; en la siguiente ejecución el orquestador cargará automáticamente y expondrá la nueva entrada.

Como cada agente es puro JSON, puedes extender el enjambre con expertos en QA, marketing, redacción técnica, manipulación de datos o cualquier otro proceso que quieras automatizar en tu IDE.

## Más allá del desarrollo

Aun cuando Codex Agents Swarm se siente cómodo implementando código, nada restringe a los agentes a tareas de desarrollo. Al definir flujos de trabajo en JSON puedes crear:

- Agentes de investigación que resuman documentación antes de programar.
- Revisores de cumplimiento que verifiquen commits para detectar violaciones de políticas.
- Runbooks operativos que coordinen despliegues o respuesta ante incidentes.
- Bots de documentación que mantengan sincronizados los changelogs y READMEs.

Si el complemento OpenAI Codex puede acceder al repositorio desde tu IDE, puede orquestar estos agentes mediante el mismo marco.
