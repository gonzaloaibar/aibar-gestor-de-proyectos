**DOCUMENTASION DE REQUISITOS DEL SISTEMA (aibar)**  
   
Introducción  
El presente documento describe los requisitos funcionales para el sistema-plataforma aibar.  
 A grandes rasgos el objetivo del sistema es permitir a los usuarios crear proyectos colaborativos con un equipo de trabajo para asignar tareas y documentar el progreso del proyecto.  
   
Entidades Principales  
- Usuario  
- Espacio de trabajo (Workspace)  
- Membresía de espacio de trabajo (relaciona Usuario con Workspace, con rol y estado)  
- Proyecto  
- Tablero (Board)  
- Lista / panel (BoardList)  
- Tarea  
- Comentario (post-MVP)  
- Etiqueta (post-MVP; en el MVP la importancia de una tarea se indica con su prioridad)  
   
Requisitos funcionales del Sistema  
   
- Un Usuario puede iniciar sesión / registrarse.  
- Un Usuario puede crear un espacio de trabajo y pasa a ser su Owner.  
- Un Usuario con permisos (Owner/Admin) puede crear un proyecto dentro de un espacio de trabajo.  
- Un Usuario con permisos (Owner/Admin/Member) puede invitar a otros usuarios registrados al espacio de trabajo.  
- Un espacio de trabajo puede tener muchos proyectos.  
- Un proyecto puede tener tableros, y los tableros listas con tareas.  
- Las tareas estarán en listas (paneles) que indican su estado (por ejemplo "To Do", "In Progress", "Done").  
- Los usuarios con permisos (Owner/Admin) pueden crear las listas.  
- Una tarea puede tener varios asignados.  
- Los usuarios de mayor rango (Owner/Admin) pueden asignar tareas a otros usuarios.  
- Un usuario con rol Member puede asignarse una tarea a sí mismo si lo desea.  
- Los usuarios de mayor rango (Owner/Admin) pueden asignar roles a los demás, según las reglas de jerarquía.  
- Los usuarios de mayor rango (Owner/Admin) pueden banear del espacio de trabajo a otros usuarios, según las reglas de jerarquía.  
- Las tareas tienen una prioridad (Low, Medium, High, Urgent) para indicar su importancia.  
Post-MVP  
- Comentarios en tareas.  
- Etiquetas para clasificar tareas (crear/editar etiquetas y aplicarlas a tareas, solo Owner/Admin).  
   
   
Requisitos No Funcionales  
- Arquitectura  
  - Implementar arquitectura REST  
   
- Frameworks  
  - Implementar DJANGO y DJANGO REST  
   
- Seguridad  
  - Usar autenticación mediante JWT  
  - Permisos personalizados a nivel de objeto  
  - Throttling básico  
  - CORS bien configurado  
   
- Persistencia  
  - Toda la información deberá almacenarse en una base de datos relacional gestionada por PostgreSQL  
   
Reglas de negocio  
1. Un usuario no puede ingresar a un espacio de trabajo al que no fue invitado.  
2. Un usuario no puede cambiar el estado de una tarea si no le pertenece (no es creador ni asignado), a menos que sea Admin/Owner del espacio de trabajo. Los roles existen solo a nivel de espacio de trabajo; no hay roles por proyecto.  
3. Un usuario no puede crear tareas a menos que tenga los permisos correspondientes (rol Member o superior).  
4. Un usuario no puede crear proyectos en un espacio de trabajo si no tiene los permisos correspondientes (rol Admin o superior en ese espacio).  
5. Cuando un usuario es baneado, se lo quita de los asignados de las tareas de ese espacio de trabajo. Una tarea queda huérfana solo si se queda sin ningún asignado, y queda disponible para que otro usuario la tome o se la asignen.  
6. Una tarea puede tener varios asignados, y solo pueden asignarse usuarios con membresía activa en el espacio de trabajo.  
7. **Invitación:** invitar a un usuario crea su membresía en estado active a partir del email de un usuario ya registrado. No existe un estado intermedio de "invitación pendiente" en el MVP.  
8. **Jerarquía:** un usuario no puede banear, ni cambiar el rol o el estado de otro usuario cuyo rango sea igual o mayor al suyo. Ejemplo: un Admin no puede modificar a otro Admin ni al Owner.  
9. **Owner:** el Owner es intocable (no puede ser baneado ni degradado por otros usuarios). Solo existe un Owner por espacio de trabajo: su creador. Nadie, ni siquiera el Owner, puede asignar el rol Owner a otro usuario a través de la API. Un espacio de trabajo siempre tiene un Owner.   
10. **Ban:** banear equivale a cambiar el estado de la membresía a suspended. Un usuario con membresía no activa no puede acceder al espacio de trabajo.  
   
Permisos  
Los permisos se establecen según los siguientes roles: Owner (dueño), Admin, Menber, Viewer  
  
|  |  |  |  |  |  
| - | - | - | - | - |  
| **Acción** |  **Owner** |  **Admin** |  **Member** |  **Viewer** |  
| Editar Workspace |  Sí |  Sí |  No |  No |  
| Eliminar Workspace |  Sí |  No |  No |  No |  
| Invitar miembros |  Sí |  Sí |  Sí |  No |  
| Banear miembros / cambiar status de un usuario |  Sí |  Sí, solo a usuarios de rango menor |  No |  No |  
| Cambiar rol a otro usuario |  Sí, pero sin asignar Owner |  Sí, solo a usuarios de rango menor y sin asignar Owner |  No |  No |  
| Crear/editar/eliminar proyecto |  Sí |  Sí |  No |  No |  
| Crear/eliminar board o lista |  Sí |  Sí |  No |  No |  
| Crear tarea |  Sí |  Sí |  Sí |  No |  
| Cambiar estado/lista de tarea |  Sí |  Sí |  Sí, si es creador o la tiene asignada |  No |  
| Editar tarea (campos) |  Sí |  Sí |  Sí, si es creador o la tiene asignada |  No |  
| Eliminar tarea |  Sí |  Sí |  Sí, si es creador |  No |  
| Asignar tarea a otro usuario |  Sí |  Sí |  No |  No |  
| Asignarse una tarea a sí mismo |  Sí |  Sí |  Sí |  No |  
  
   
Todos los roles con membresía activa pueden leer (ver) el contenido del espacio de trabajo, incluido Viewer.  
Acciones post-MVP (etiquetas):  
  
|  |  |  |  |  |  
| - | - | - | - | - |  
| **Acción** |  **Owner** |  **Admin** |  **Member** |  **Viewer** |  
| Crear/editar etiquetas |  Sí |  Sí |  No |  No |  
| Aplicar etiqueta existente a tarea |  Sí |  Sí |  No |  No |  
  
   
Diseño de Test  
- Usuario no autenticado → 401.  
- Usuario intenta acceder a un Workspace al que no fue invitado → 403.  
- Owner crea un Workspace/Proyecto/Lista/Tarea → 201.  
- Member intenta editar/eliminar Workspace → 403.  
- Admin edita Workspace → 200.  
- Admin intenta eliminar Workspace → 403.  
- Member puede crear tarea → 201.  
- Viewer intenta crear tarea/proyecto/lista → 403.  
- Viewer puede leer el contenido del Workspace → 200.  
- Viewer intenta realizar cualquier escritura → 403.  
- Admin intenta cambiar estado de tarea → 200.  
- Member intenta modificar/eliminar tarea que no le pertenece → 403.  
- Admin edita/elimina proyecto/tarea/lista/tablero → 200/204.  
- Member intenta asignar tarea a otro usuario → 403.  
- Member invita a un usuario → 201.  
- Member intenta banear o cambiar rol de otro usuario → 403.  
- Admin intenta banear o cambiar rol a otro Admin o al Owner → 403.  
- Admin banea a un Member → 200.  
- Se banea a un usuario que era el único asignado → la tarea queda sin asignados.  
- Se banea a un usuario que compartía la tarea con otros → deja de figurar en assignees y los demás se mantienen.  
- Usuario baneado intenta acceder al Workspace → 403.  
- Intentar asignar una tarea a un usuario sin membresía activa en el Workspace → 400.  
   
