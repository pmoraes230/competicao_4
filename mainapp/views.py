from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import uuid
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.utils import timezone
from . import models

def get_user_profile(request):
    user_id = request.session.get("user_id")
    if user_id:
        try:
            user = models.Usuario.objects.select_related('perfil').get(id=user_id)
            return {
                'user_id': user.id,
                'user_name': user.nome,
                'user_role': user.perfil.nome,
                'is_authenticaded': True
            }
        except models.Usuario.DoesNotExist:
            return {'user_name': '', 'is_authenticaded': False}
    return {'user_name': '', 'is_authenticaded': False}

def login(request):
    if request.method == "GET":
        return render(request, "login/login.html")
    
    login = request.POST.get("login")
    password = request.POST.get("senha")
    if not all([login, password]):
        messages.error(request, "Todos os campos são necessários")
        return redirect("login")
    try:
        user = models.Usuario.objects.filter(email=login).first() or models.Usuario.objects.filter(cpf=login).first()
        if not user:
            messages.error(request, "Informe seu email ou CPF como login")
            return redirect("login")
        
        if check_password(password, user.senha):
            request.session['user_id'] = user.id
            request.session['user_name'] = user.nome
            request.session['user_role'] = user.perfil.nome
            
            messages.success(request, f"Bem vindo {user.nome}!")
            if user.perfil.nome == 'Totem':
                return redirect("totem")
            return redirect("home")
    except models.Usuario.DoesNotExist:
        messages.error(request, "Erro ao encontrar usuário.")
        return redirect("login")
    
def logoutPage(request):
    logout(request)
    messages.success(request, "Saindo do sistema")
    return redirect("login")
    
def home(request):
    context = get_user_profile(request)
    event = models.Evento.objects.all()
    
    context['events'] = event
    
    return render(request, "home/home.html", context)

def register_event(request):
    context = get_user_profile(request)
    if request.method == "POST":
        name_event = request.POST.get("name")
        date_event = request.POST.get("date")
        time_event = request.POST.get("time")
        limit_peaple = request.POST.get("limit_peaple")
        price_event = request.POST.get("price")
        image_event = request.FILES.get("image")
        describle_event = request.POST.get("describle")
        
        if not all([name_event, date_event, time_event, limit_peaple, price_event, image_event, describle_event]):
            messages.error(request, "Todos os campos são obrigatórios")
            return redirect("register_event")
        
        if models.Evento.objects.filter(dia=date_event, horario=time_event).exists():
            messages.error(request, "Data e horário já ocupada com outro evento")
            return redirect("register_event")
        
        
        user_id = request.session.get("user_id")
        if not user_id:
            messages.error(request, "Usuário não autenticado")
            return redirect("login")
        
        try:
            user = models.Usuario.objects.get(id=user_id)
        except models.Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado")
            return redirect("login")
        
        try:
            new_event = models.Evento.objects.create(
                nome=name_event,
                dia=date_event,
                horario=time_event,
                cpt_evento=limit_peaple,
                preco=price_event,
                usuario=user,
                imagem=image_event,
                descricao=describle_event
            )
            new_event.full_clean()
            new_event.save()
            
            messages.success(request, "Evento Cadastrado com sucesso.")
            return redirect("register_setor")
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar evento: {str(ve)}")
            return redirect("register_event")
    return render(request, "register_event/register_event.html", context)

def update_event(request, id_event):
    context = get_user_profile(request)
    try:
        event = models.Evento.objects.get(id=id_event)
    except models.Evento.DoesNotExist:
        messages.error(request, "Evento não encontrado")
        return redirect("details_event", id_event=id_event)
        
    if request.method == "POST":
        name_event = request.POST.get("name")
        date_event = request.POST.get("date")
        time_event = request.POST.get("time")
        limit_peaple = request.POST.get("limit_peaple")
        price_event = request.POST.get("price")
        image_event = request.FILES.get("image")
        describle_event = request.POST.get("describle")
        
        if not all([name_event, date_event, time_event, limit_peaple, price_event, describle_event]):
            messages.error(request, "Todos os campos são obrigatórios")
            return redirect("update_event", id_event=id_event)
        
        if models.Evento.objects.filter(dia=date_event, horario=time_event).exclude(id=id_event).exists():
            messages.error(request, "Data e horário já ocupada com outro evento")
            return redirect("register_event")
        
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "Usuário não logado.")
            return redirect("login")
        
        try:
            user = models.Usuario.objects.get(id=user_id)
        except models.Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado")
            return redirect("login")
            
        event.nome = name_event
        event.dia = date_event
        event.horario = time_event
        event.cpt_evento = limit_peaple
        event.preco = price_event
        event.usuario = user
        if image_event:
            event.imagem = image_event
        event.descricao = describle_event
        
        event.full_clean()
        event.save()
        
        messages.success(request, f"Evento {event.nome} atualizado com sucesso.")
        return redirect("details_event", id_event=id_event)
        
    context.update({
        'event': event
    })
    return render(request, "register_event/update_event.html", context)

def delete_event(request, id_event):
    try:
        event = models.Evento.objects.get(id=id_event)
        if request.method == "POST":
            event.delete()
            messages.success(request, "Evento apagado do sistema.")
            return redirect("home")
        context = {
            'event': event,
            **get_user_profile(request)
        }
        return render(request, "register_event/delete_event.html", context)
    except models.Evento.DoesNotExist:
        messages.error(request, "Evento não encontrado")
        return redirect("home")

def register_setor(request):
    context = get_user_profile(request)
    context['events'] = models.Evento.objects.all()
    
    if request.method == "POST":
        name_setor = request.POST.get("name")
        limit_ticket = request.POST.get("limit_ticket")
        id_event = request.POST.get("event")
        
        if not all([name_setor, limit_ticket, id_event]):
            messages.error(request, "Todos os campos são obrigatórios")
            return redirect("register_setor")
        
        try:
            event = models.Evento.objects.get(id=id_event)
        except models.Evento.DoesNotExist:
            messages.error(request, "Evento não encontrado.")
            return redirect("register_setor")
        
        try:
            new_setor = models.Setor.objects.create(
                nome=name_setor,
                qtd_setor=limit_ticket,
                evento=event
            )
            new_setor.full_clean()
            new_setor.save()
            
            messages.success(request, "Setor Salvo com sucesso.")
            return redirect("home")
        except ValueError as ve:
            messages.error(request, f"Erro ao salvar setor: {str(ve)}")
            return redirect("register_setor")
    
    return render(request, "register_setor/register_setor.html", context)

def deteils_event(request, id_event):
    context = get_user_profile(request)
    
    try:
        event = models.Evento.objects.get(id=id_event)
        setors = models.Setor.objects.filter(evento=id_event)
        cliente = None
        clientes_encontrados = []
        
        if request.method == 'POST' and 'search_client' in request.POST:
            search_client = request.POST.get("pesquisa_cliente", "").strip()
            if search_client:
                clientes_encontrados = models.Cliente.objects.filter(
                    Q(nome__icontains=search_client)
                )[:10]
                if not clientes_encontrados:
                    messages.info(request, f"Nenhum cliente encontrado para o termo '{search_client}'")
                else:
                    messages.success(request, f"{clientes_encontrados.count()} cliente(s) encontrado(s).")
            else:
                messages.error(request, "Digite um nome para a pesquisa")
            
        if request.method == 'POST' and 'select_client' in request.POST:
            client_id = request.POST.get("client_id")
            print(client_id)
            try:
                cliente = models.Cliente.objects.get(id=client_id)
                messages.success(request, f"Cliente {cliente.nome} selecionado")
            except models.Cliente.DoesNotExist:
                messages.error(request, "Cliente não encontrado.")
        
        context.update({
            'event': event,
            'setors': setors,
            'cliente': cliente,
            'clientes_encontrados': clientes_encontrados,
            'pesquisa_cliente': request.POST.get("pesquisa_cliente", "")
        })
        
        return render(request, "register_event/details_event.html", context)
    except models.Evento.DoesNotExist:
        messages.error(request, "Evento não encontrado")
        return redirect("home")    
    
def buy_ticket(request, id_event):
    try:
        event = models.Evento.objects.get(id=id_event)
        setors = models.Setor.objects.filter(evento=id_event)
        client = None
        
        if request.method == 'POST' and 'buy_ticket' in request.POST:
            client_id = request.POST.get("cliente_id")
            if not client_id:
                messages.info(request, "Por favor, selecionar um cliente.")
                return redirect("details_event", id_event=id_event)
            try:
                client = models.Cliente.objects.get(id=client_id)
            except models.Cliente.DoesNotExist:
                messages.info(request, "Cliente não encontrado.")
                return redirect("details_event", id_event=id_event)
            
            setor_form = request.POST.get("setor")
            amount = int(request.POST.get("amount", 0))
            
            if not setor_form:
                messages.info(request, "Por favor, selecione um setor")
                return redirect("details_event", id_event=id_event)
            try:
                setor = models.Setor.objects.get(id=setor_form)
            except models.Setor.DoesNotExist:
                messages.error(request, "Setor não encontrado.")
                return redirect("details_event", id_event=id_event)
            
            if amount < 1:
                messages.info(request, "A quantidade deve ser pelo menos 1 ingresso.")
                return redirect("details_event", id_event=id_event)
            elif amount > 10:
                messages.info(request, "Limite máximo de ingresso para compra é 10")
                return redirect("details_event", id_event=id_event)
            elif setor.qtd_setor < amount:
                messages.info(request, f"Não há ingressos suficientes no setor {setor.nome}.")
                return redirect("details_event", id_event=id_event)
            else:
                tickets = []
                for _ in range(amount):
                    ticket = models.Ingresso.objects.create(
                        id_ingresso=str(uuid.uuid4()),
                        cliente=client,
                        evento=event,
                        setor=setor,
                        data_emissao=timezone.now(),
                        valor=event.preco or 0.00,
                        status_ingresso='emitido'
                    )
                    tickets.append(ticket)
                    setor.qtd_setor -= 1
                    setor.save()
                
                # Gerar o PDF com os ingressos
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="ingressos_evento_{event.id}.pdf"'
                
                # Criar o documento PDF
                doc = SimpleDocTemplate(response, pagesize=A4)
                elements = []
                
                styles = getSampleStyleSheet()
                style_normal = styles['Normal']
                style_heading = styles['Heading1']
                
                # Para cada ingresso, adicionar uma seção ao PDF
                for ticket in tickets:
                    elements.append(Paragraph(f"Ingresso para {event.nome}", style_heading))
                    elements.append(Spacer(1, 0.5 * cm))
                    elements.append(Paragraph(f"Cliente: {ticket.cliente.nome}", style_normal))
                    elements.append(Paragraph(f"Setor: {ticket.setor.nome}", style_normal))
                    elements.append(Paragraph(f"Data de Emissão: {ticket.data_emissao.strftime('%d/%m/%Y %H:%M')}", style_normal))
                    elements.append(Paragraph(f"Valor: R$ {ticket.valor:.2f}", style_normal))
                    elements.append(Paragraph(f"ID do Ingresso: {ticket.id_ingresso}", style_normal))
                    elements.append(Spacer(1, 1 * cm))
                    elements.append(Paragraph("-" * 50, style_normal))  # Separador entre ingressos
                
                # Construir o PDF
                doc.build(elements)
                
                messages.success(request, f"Compra realizada com sucesso para {client.nome} no evento {event.nome}.")
                return response
                
        context = {
            'event': event,
            'setors': setors,
            'cliente': client,
            'clientes_encontrados': [],
            'pesquisa_cliente': request.POST.get("pesquisa_cliente", ""),
            **get_user_profile(request)
        }
        return render(request, "register_event/details_event.html", context)
                    
    except models.Evento.DoesNotExist:
        messages.error(request, "Evento não encontrado.")
        return redirect("home")
    
def list_setor(request):
    context = {
        'setors': models.Setor.objects.all(),
        **get_user_profile(request)
    }
    
    return render(request, "register_setor/list_setor.html", context)

def update_setor(request, id_setor):
    context = get_user_profile(request)
    
    try:
        setor = models.Setor.objects.get(id=id_setor)
    except models.Setor.DoesNotExist:
        messages.error(request, "Setor não encontrado.")
        return redirect("list_setor")
   
    if request.method == "POST":
        name_setor = request.POST.get("name")
        limit_ticket = request.POST.get("limit_ticket")
        select_event = request.POST.get("event")
        
        if not all([name_setor, limit_ticket, select_event]):
            messages.info(request, "Todos os campos são de preenchimento obrigatórios")
            return redirect("update_setor", id_setor=id_setor)
        
        try: 
            event = models.Evento.objects.get(nome=select_event)
        except models.Evento.DoesNotExist:
            messages.info(request, "Evento não encontrado")
            return redirect("update_setor", id_setor=id_setor)
        
        try:
            setor.nome = name_setor
            setor.qtd_setor = limit_ticket
            setor.evento = event
            
            setor.full_clean()
            setor.save()
            
            messages.success(request, "Setor atualizado com sucesso.")
            return redirect("list_setor")
            
        except ValueError as ve:
            messages.error(request, f"Erro ao atualizar setor: {str(ve)}")
            return redirect("update_setor", id_setor=id_setor)
    
    context.update({
        'setor': setor
    })
    return render(request, "register_setor/update_setor.html", context)

def delete_setor(request, id_setor):
    try:
        setor = models.Setor.objects.get(id=id_setor)
        if request.method == "POST":
            setor.delete()
            messages.success(request, "Setor deletado com sucesso.")
            return redirect("list_setor")
        context = {
            'setor': setor,
            **get_user_profile(request)
        }
        
        return render(request, "register_setor/delete_setor.html", context)
    except models.Setor.DoesNotExist:
        messages.error(request, "Setor não encontrado")
        return redirect("list_setor")

def list_user(request):
    context = {
        'users': models.Usuario.objects.all(),
        **get_user_profile(request)
    }
    
    return render(request, "user/list_user.html", context)

def register_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        id_perfil = request.POST.get("perfil")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        if not all({name, email, cpf, id_perfil, password1, password2}):
            messages.info(request, "Todos os campos são obrigatórios")
            return redirect("register_user")
        
        if password1 != password2:
            messages.info(request, "Senhas diferentes")
            return redirect("register_user")
        
        if models.Usuario.objects.filter(cpf=cpf).exists():
            messages.info(request, "Usuário já cadastrado")
            return redirect("register_user")
        
        if models.Usuario.objects.filter(email=email).exists():
            messages.info(request, "Email já cadastrado")
            return redirect("register_user")
        
        try:
            perfil = models.Perfil.objects.get(id=id_perfil)
            hashers_password = make_password(password1)
            
            new_user = models.Usuario.objects.create(
               nome=name,
               email=email,
               cpf=cpf,
               senha=hashers_password,
               perfil=perfil 
            )
            new_user.full_clean()
            new_user.save()
            
            messages.success(request, f"{new_user.nome} cadastrado com sucesso.")
            return redirect("list_user")
            
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar novo usuário: {str(ve)}")
    
    context = {
        'perfis': models.Perfil.objects.all(),
        **get_user_profile(request)
    }
    
    return render(request, "user/register_user.html", context)

def update_user(request, id_user):
    try:
        user = models.Usuario.objects.get(id=id_user)
    except models.Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado")
        return redirect("list_user")
    
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        id_perfil = request.POST.get("perfil")
        
        if not all([name, email, cpf, id_perfil]):
            messages.info(request, "Todos os campos são obrigatórios")
            return redirect("update_user", id_user=id_user)
        
        if models.Usuario.objects.filter(email=email).exclude(id=id_user).exists():
            messages.info(request, "Email já cadastrado")
            return redirect("update_user", id_user=id_user)
        
        try:
            perfil = models.Perfil.objects.get(id=id_perfil)
            
            user.nome = name
            user.email = email
            user.cpf = cpf
            user.perfil = perfil
            
            user.full_clean()
            user.save()
            
            messages.success(request, f"Cadastro de {user.nome} atualizado com sucesso!")
            return redirect("list_user")
        except ValueError as ve:
            messages.error(request, f"Erro ao atualizar usuário: {str(ve)}")
    
    context =  {
        'perfis': models.Perfil.objects.all(),
        'user': user,
        **get_user_profile(request)
    }
    
    return render(request, "user/update_user.html", context)

def delete_user(request, id_user):
    try:
        user = models.Usuario.objects.get(id=id_user)
        if request.method == "POST":
            user.delete()
            messages.success(request, "Usuário apagado do sistema.")
            return redirect("list_user")
        context = {
            'user': user,
            **get_user_profile(request)
        }
        
        return render(request, "user/delete_user.html", context)
    except models.Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect("list_user")
    
def list_client(request):
    context = {
        'clients': models.Cliente.objects.all(),
        **get_user_profile(request)
    }
    
    return render(request, "client/list_client.html", context)

def register_client(request):
    context = get_user_profile(request)
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        
        if not all([name, email, cpf]):
            messages.info(request, "Todos os campos são obrigatórios")
            return redirect("register_client")
        
        if models.Cliente.objects.filter(cpf=cpf).exists():
            messages.info(request, "CPF já cadastrado")
            return redirect("register_client")
            
        try:
            new_client = models.Cliente.objects.create(
                nome=name,
                cpf=cpf,
                email=email
            )
            new_client.full_clean()
            new_client.save()
            
            messages.success(request, f"Cliente {new_client.nome} cadastrado com sucesso.")
            return redirect("home")
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar o cliente: {str(ve)}")
            return redirect("register_client")
    
    return render(request, "client/register_client.html", context)

def update_client(request, id_client):
    try:
        client = models.Cliente.objects.get(id=id_client)
    except models.Cliente.DoesNotExist:
        messages.error(request, "Cliente não encontrado")
        return redirect("list_client")
    
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        
        if not all([name, email, cpf]):
            messages.info(request, "Todos os campos são obrigatórios")
            return redirect("update_client", id_client=id_client)
        
        if models.Cliente.objects.filter(cpf=cpf).exclude(id=id_client).exists():
            messages.info(request, "CPF já cadastrado")
            return redirect("update_client", id_client=id_client)
        
        try:
            client.nome = name
            client.email = email
            client.cpf = cpf
            
            client.full_clean()
            client.save()
            
            messages.success(request, f"Cadastro do cliente {client.nome} atualizado com sucesso.")
            return redirect("list_client")
        except ValueError as ve:
            messages.error(request, f"Erro ao atualizar cliente: {str(ve)}")
            return redirect("update_client", id_client=id_client)
    
    context = {
        'client': client,
        **get_user_profile(request)
    }
    
    return render(request, "client/update_client.html", context)

def delete_client(request, id_client):
    try:
        client = models.Cliente.objects.get(id=id_client)
        if request.method == "POST":
            client.delete()
            messages.success(request, "Cliente apagado do sistema.")
            return redirect("list_client")
        context = {
            'client': client,
            **get_user_profile(request)
        }
        return render(request, "client/delete_client.html", context)
    except models.Cliente.DoesNotExist:
        messages.error(request, "Cliente não encontrado")
        return redirect("list_client")
    
