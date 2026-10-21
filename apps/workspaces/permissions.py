#este metodo es un atajo que busca un objeto en la BD y si no lo encuentra lanza automaticamente 404
from django.shortcuts import get_object_or_404
from django.utils import cache
#BasePermission es la clase base de permisos, me permite crear reglas personalizadas para el user
#SAFE_METHODS es una tupla que contiene los metods http seguros ('GET', 'HEAD', 'OPTIONS')
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Workspace, WorkspaceMemberShip

Role=WorkspaceMemberShip.role
Status=WorkspaceMemberShip.status


# ------------------------------------------------------------------
# Helpers: Basicamente funciones que se ejecutaran constantemente para validar permiso
# ------------------------------------------------------------------

#este metodo tomara el workspace de la url
def get_workspace(request, view):
    #obtengo el slug atravez de la instancia de la vista
    slug = view.kwargs.get('slug')

    if slug is None:
        return None

    #request.__dict__ es el diccionario de atributos del objeto request
    #setdefault crea un diccionario vacio si todavia no existe, ese diccionario sera el cache, ahi estaran los request realizados
    #uso cache porque en cada peticion DRF llama a los permisos, y cada uno necesita workspace y la membresia, sin cache se hace la misma consulta varias veces
    cache = request.__dict__.setdefaul('_aibar_workspaces', {})

    if slug not in cache:
        #Aquí finalmente consulta el modelo Workspace, y lo guarda en el diccionario cache
        cache[slug]=get_object_or_404(Workspace, slug=slug)

    #se retorna el objeto workspace correspondiente con el slug, recuerda que cache podria tener mas de un objeto, por eso se lo especifica con la clave que sera slug
    return cache[slug]

#este metodo obtiene la membresia ACTIVA del usuario o None, cacheada por request
def get_membership(request, workspace):

    #obtengo el usuario de la request, verifico que me devuelva algo y que este autenticado
    user = request.user
    if not user or not user.is_authenticated:
        return None

    #mismo procedimiento que en el metodo get_workspace
    cache = request.__dict__.setdefaul('_aibar_memberships', {})

    #por si esta request no se hizo aun pregunto si el workspace no esta en la cache
    if workspace.pk not in cache:
        cache[workspace.pk]=WorkspaceMemberShip.objects.filter(workspace=workspace, user=user, status=Status.ACTIVE).first()

    return cache[workspace.pk]

# ------------------------------------------------------------------
# Configuracion de permisos para los workspaces
'''
    - Lectura (GET/HEAD/OPTIONS): cualquier miembro activo (incluye Viewer).
    - Escritura: rol >= min_role.
    - Sin membresía activa (no invitado / baneado): 403.
    - Rutas sin workspace en la URL (list/create de workspaces): pasa;
      el queryset debe filtrar por las membresías del usuario.
'''
# ------------------------------------------------------------------

class WorkspaceRolePermission(BasePermission):

    min_role=Role.MEMBER
    messaje='No tenés permisos para realizar esta acción en este espacio de trabajo.'

    #este metodo es basicamente para preguntar si la request tiene permisos para acceder a la vista
    def has_permission(self, request, view):
        workspace = get_workspace(request, view)
        if workspace is None:
                return True #si url no esta asociada a un workspace no hay nada que comprobar
        membership = get_membership(request, workspace)
        if membership is None:
            return False

        #si el metodo es de lectura se requiere que el rol sea almenos viewer, si no debe ser almenos Member
        required = Role.VIEWER if request.method in SAFE_METHODS else self.min_role
        #retorna true o false respectivamente
        return membership.role >= required


#si su Role es MEMBER
class MemberCanWrite(WorkspaceRolePermission):
    min_role = Role.MEMBER  # crear tareas, autoasignarse

#si su Role es ADMIN
class AdminCanWrite(WorkspaceRolePermission):
    min_role = Role.ADMIN  # proyectos, boards/listas, asignar a otros

#si su Role es OWNER
class OwnerCanWrite(WorkspaceRolePermission):
    min_role = Role.OWNER   # eliminar workspace

# ------------------------------------------------------------------
# configuracion de permisos para los projects
'''
Lectura: cualquier miembro activo.
Crear/editar/eliminar proyecto: solo Admin y Owner.
A nivel objeto verifica que el proyecto pertenezca al workspace de la URL.
'''
# ------------------------------------------------------------------

#heredando de AdminCanWrite ya que el crud esta permitido solo para Admin y Owner
class ProjectPermission(AdminCanWrite):

    def has_object_permission(self, request, view, obj):
        workspace = get_workspace(request, view)
        return workspace is not None and obj.workspace == workspace.pk
