# Guía para manejar ramas en GitHub y VSCode

## 1. Crear una nueva rama desde la terminal de VSCode

1. Asegúrate de estar en la rama principal (generalmente `main` o `master`):
   ```
   git checkout main
   ```

2. Actualiza tu rama principal:
   ```
   git pull
   ```

3. Crea una nueva rama:
   ```
   git checkout -b nombre-de-la-rama
   ```

## 2. Subir la rama a GitHub desde la terminal de VSCode

1. Realiza tus cambios y haz commit:
   ```
   git add .
   git commit -m "Descripción de tus cambios"
   ```

2. Sube la rama a GitHub:
   - La primera vez que subas una rama, debes especificar el nombre de la rama:
     ```
     git push --set-upstream origin nombre-de-la-rama
     ```
   - Para las siguientes actualizaciones:
     ```
     git push
     ```

## 3. Fusionar (merge) la rama desde GitHub

1. Ve a la página de tu repositorio en GitHub.

2. Pulsa el botón 'Compare & pull request' que aparece junto a tu rama recién subida.

3. Revisa los cambios y añade un título y descripción para tu pull request.

4. Pulsa 'Create pull request' para iniciar el proceso de revisión.

5. Si no hay conflictos y tienes los permisos necesarios, verás el botón 'Merge pull request'. Púlsalo.

6. Confirma el merge pulsando 'Confirm merge'.

7. Una vez completado el merge, verás la opción de 'Delete branch'. Púlsala si ya no necesitas la rama en GitHub.

## 4. Actualizar y limpiar tu repositorio local

1. Cambia a la rama principal en tu repositorio local:
   ```
   git checkout main
   ```

2. Actualiza tu rama principal local con los cambios de GitHub:
   ```
   git pull
   ```

3. Borra la rama local que ya has fusionado:
   ```
   git branch -d nombre-de-la-rama
   ```

## Notas adicionales

- Asegúrate de reemplazar `nombre-de-la-rama` con el nombre real de tu rama en todos los comandos.
- Siempre es una buena práctica crear una nueva rama para cada nueva función o corrección que estés desarrollando.
- Antes de crear un pull request, asegúrate de que tu código esté bien comentado y siga las convenciones de estilo de tu equipo.
- Si surgen conflictos durante el merge, tendrás que resolverlos manualmente antes de poder completar el proceso.


## Configuración de alias en .gitconfig
- [alias]
   - tree = ls-tree --full-tree -r --name-only HEAD
	- logx = "!git log --oneline --graph --decorate --color --all | cat"
	- ch = checkout
	- br = branch
	- acp = "!f() { git add . && git commit -m \"$@\" && git push; }; f"
