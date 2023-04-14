# HamRadioRecorder
Modificación del script original https://github.com/Jipok/icecast_recorder/blob/master/icecast_recorder.py. 
Se le agrego: 
 * Una barra de progreso
 * Un parámetro adicional para establecer el tiempo de grabación en segundos
 * Tiempo trascurrido de grabación
 * Un nombre de archivo harcodeado con la fecha y la hora de grabación
Modo de uso: icecast_recorder.py <url> <duración en segundos>

Para grabar el programa Contactos lo uso asi:

python record2023.py http://generalrodriguez.gob.ar:8000/radio 3600
