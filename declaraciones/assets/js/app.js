import "../scss/app.scss";

window.$ = window.jQuery = require('jquery');
import Popper from 'popper.js';
import 'jquery-ui/ui/widgets/datepicker';
import 'bootstrap';
import 'select2';
import 'eonasdan-bootstrap-datetimepicker';
import 'selectize/dist/js/standalone/selectize.min.js';
require('./declaracion/loader')
require('./svg');
require('./sidebar');
require('./tooltip');
require('./declaracion/login')
require('./declaracion/validacion')
require('./declaracion/datepicker')
window.dui=require('./declaracion/widgets')
require('./declaracion/nacionalidades')
require('./declaracion/no_aplica')
require('jquery.are-you-sure/ays-beforeunload-shim')
require('jquery.are-you-sure/jquery.are-you-sure')
require('./declaracion/areyousure')
require('./declaracion/enter-key')
require('./declaracion/impresion')
