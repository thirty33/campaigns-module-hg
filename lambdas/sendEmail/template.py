# archivo_html.py

def export_html(object):

    styles = """
        <style type="text/css">
            @media (max-width: 375px) {
                .header-items {
                    display: none;
                }

                .container-title {
                    width: 115px !important;
                }

                .logo {
                    width: 80px !important;
                }

                .title {
                    font-size: 15px !important;
                    margin-top: 20px !important;
                }

                p {
                    margin-left: 0 !important;
                    font-size: 10px !important;
                }

                .title {
                    font-size: 15px !important;
                    margin-top: 20px !important;
                }

                table {
                    margin-top: 10px;
                }

                td,
                th {
                    width: auto;
                }

                .data-table {
                    width: 89% !important;
                }
            }

            @media (max-width: 570px) {
                .header-items {
                    display: none;
                }

                .container-title {
                    width: 115px !important;
                }

                .logo {
                    width: 80px !important;
                }

                .title {
                    font-size: 15px !important;
                    margin-top: 20px !important;
                }

                p {
                    margin-left: 0 !important;
                    font-size: 10px !important;
                }

                .title {
                    font-size: 15px !important;
                    margin-top: 20px !important;
                }

                table {
                    margin-top: 10px;
                }

                td,
                th {
                    width: auto;
                }
            }

            @media (max-width: 575px) {
                .data-table {
                    width: 80%;
                }
            }

            @media (min-width: 576px) and (max-width: 767px) {
                .data-table {
                    width: 80%;
                }
            }

            @media (min-width: 768px) and (max-width: 991px) {
                .data-table {
                    width: 50%;
                }
            }

            @media (min-width: 992px) and (max-width: 1199px) {
                .data-table {
                    width: 50%;
                }
            }

            @media (min-width: 1200px) and (max-width: 1399px) {
                .data-table {
                    width: 50%;
                }
            }

            @media (min-width: 1400px) {
                .data-table {
                    width: 50%;
                }
            }

            .title {
                font-size: 18px;
                margin-top: 40px;
            }

            table {
                margin-top: 18px;
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }

            .data-table td {
                border: 1px solid #ccc;
                text-align: left;
                padding: 8px;
                width: 200px;
            }

            th {
                border: 1px solid #ccc;
                text-align: left;
                padding: 8px;
                width: 150px;
            }

            p {
                text-align: justify;
                font-size: 10px;
            }

            .data-table {
                border: hidden !important;
            }
        </style>
    """

    html_code = f"""
        <!DOCTYPE html>
        <html lang="en">
        
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Confirmación de correo</title>

            {styles}

        </head>

        <body>

            <body style="margin: 0; padding: 0; box-sizing: border-box; height: auto;">

                <header style="display: inline-block; width: 100%; background-color: #f2e2e2; margin-top: 0;"
                    class="header-items">
                    <table style="width:100%;">
                        <tr>
                            <td class="container-title" style="border: none; width: 250px;
                        ">
                                <img class="logo" style="width: 120px;"
                                    src="https://mcusercontent.com/8e5276b7b5a315e4837e11841/images/af3c0f37-140d-71ba-3e70-3922d38bf4d0.png"
                                    alt="Logo">
                            </td>
                            <td style="border: none; width:350px; text-align:center;">
                                <h2 class="title">INFORMACIÓN DE TU RESERVA</h2>
                            </td>
                        </tr>
                    </table>
                </header>

                <div>
                    <h1 style="text-align:center; font-size:16px;">Apreciado cliente: <span id="name-client">{object['nombreApellido']}</span>, a continuación le anexamos la información de su reserva:</h1>
                </div>

                <table align="center" border="0" cellspacing="0" cellpadding="0" style="text-align:center;"
                    class="data-table">
                    <tr>
                        <td align="center" style="text-align:center">
                            <table border="0" cellspacing="0" cellpadding="0">
                                <tr>
                                    <th>Nombre y apellido:</th>
                                    <td id="nombreApellido">{object['nombreApellido']}</td>
                                </tr>

                                <tr>
                                    <th>Ciudad de origen:</th>
                                    <td id="ciudadOrigen">{object['ciudadOrigen']}</td>
                                </tr>

                                <tr>
                                    <th>Ciudad de destino:</th>
                                    <td id="ciudadDestino">{object['ciudadDestino']}</td>
                                </tr>

                                <tr>
                                    <th>Tipo de viaje:</th>
                                    <td id="tipoViaje">{object['tipoViaje']}</td>
                                </tr>

                                <tr>
                                    <th>Fecha de salida:</th>
                                    <td id="fechaSalida">{object['fechaSalida']}</td>
                                </tr>

                                <tr>
                                    <th>fecha de regreso:</th>
                                    <td id="fechaRegreso">{object['fechaRegreso']}</td>
                                </tr>

                                <tr>
                                    <th>Número de teléfono:</th>
                                    <td id="numeroTelefono">{object['numeroTelefonico']}</td>
                                </tr>

                                <tr>
                                    <th>Descripción:</th>
                                    <td id="descripcion">{object['Description']}</td>
                                </tr>
                            </table>

                        </td>
                    </tr>
                </table>

                <footer style="width:100%;">
                    <p style="font-family:'Zeyada', cursive; font-size:17px; text-align: center;">Génesis Suárez</p>
                    <p style="text-align:center; font-size:16px;">YOUR AGENT TRAVEL</p>
                </footer>

                <h2 style="font-size: 10px; border: none; text-align: center">Terminos y condiciones</h2>
                <table style="width:100%; margin: 10px; border: hidden !important;">
                    <tbody>
                        <tr>
                            <p>
                                1. Al solicitar una cotización de viaje con Argent Travel, el cliente acepta
                                automáticamente todos los términos y condiciones establecidos en este
                                documento.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                2. Las cotizaciones de viaje proporcionadas por Argent Travel tienen una
                                validez de 5 días a partir de la fecha de emisión. Después de este período, la
                                cotización puede estar sujeta a cambios basados en la disponibilidad y tarifas
                                actualizadas.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                3. La confirmación de la reserva se realizará una vez que el cliente haya
                                aceptado la cotización y haya realizado el pago correspondiente. Argent
                                Travelse reserva el derecho de cancelar la reserva si el pago no se recibe
                                dentro del plazo especificado.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                4. Las políticas de cancelación y reembolso estarán sujetas a las condiciones
                                establecidas por los proveedores de servicios, tales como aerolíneas, hoteles,
                                y agencias de viajes. Argent Travel no asume responsabilidad por cambios o
                                cancelaciones de servicios por parte de los proveedores.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                5. Cualquier solicitud de modificación en el itinerario después de la
                                confirmación de la reserva estará sujeta a disponibilidad y puede conllevar
                                cargos adicionales. Argent Travel no se hace responsable de cambios en el
                                itinerario realizados por terceros proveedores.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                6. El cliente es responsable de proporcionar información precisa y completa al
                                solicitar la cotización. Argent Travel no se hace responsable de problemas
                                derivados de información incorrecta proporcionada por el cliente.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                7. Se recomienda encarecidamente que el cliente adquiera un seguro de viaje
                                adecuado para cubrir posibles eventualidades, como cancelaciones, pérdida de
                                equipaje y gastos médicos.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                8. Argent Travel se reserva el derecho de modificar las tarifas y condiciones
                                en cualquier momento, previa notificación al cliente. Los cambios no afectarán
                                a las reservas ya confirmadas.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                9. Argent Travel no se hace responsable de pérdidas, daños, lesiones o gastos
                                incurridos durante el viaje, a menos que dichos incidentes sean directamente
                                atribuibles a la negligencia de la empresa.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                10. Agent Travel se reserva el derecho de aceptar seguir con el proceso de
                                viaje, y en caso contrario, desistir si de alguna manera se ve afectado el
                                trabajo que se ha realizado.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                11. De haber cancelaciones o cambios por parte del proveedor (hotel,
                                aerolínea, etc) Agent travel cumplirá con los términos que acepte el cliente,
                                ya sea por cambio de itinerario y devoluciones.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                12. Agent Travel tendrá un tiempo de hasta 90 días hábiles para realizar las
                                devoluciones, si corresponde.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                13. Agent Travel en caso de que el cliente solicite un reembolso, únicamente
                                si corresponde, de ser válido y estar aprobado por el proveedor se quedará con
                                el 5% del valor cobrado, por la gestión y procesos realizados.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                14. Un cliente no podrá desistir del viaje a menos que sea por causa de fuerza
                                mayor (demostrable), Agent Travel proporcionara alternativas al cliente.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                15. Las devoluciones sólo son válidas en determinadas situaciones, en caso de
                                que el proveedor no pueda cumplir con el servicio.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                16. Los cambios que se realicen (fecha, hotel, horarios, cambios de nombres)
                                deben ser abonados por el cliente y Agent Travel se encargará de los procesos.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                17. Agent Travel se reserva información de proveedores, datos, notificaciones
                                y documentos, que sean de uso privado entre el proveedor y la agencia.
                            </p>
                        </tr>

                        <tr>
                            <p>
                                18. Agent travel se encargará de enviar documentación de viaje un periodo de 3
                                días hábiles, siempre y cuando el viaje no esté dentro de estos días
                                estipulados, de ser un viaje cercano, Agent Travel lo enviará en el mismo día
                                de la compra.
                            </p>
                        </tr>
                    </tbody>
                </table>
            </body>

        </html>
        """
    
    return html_code