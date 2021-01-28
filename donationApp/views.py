from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from donationApp.models import Category, Institution, Donation, TYPE_CHOICES, UserProfile
from donationApp.forms import RegisterForm, LoginForm, UserUpdateForm

# Create your views here.


class LandingPage(View):
    def get(self, request):

        # stats
        institutions_count = Institution.objects.count()
        donations_count = Donation.objects.count()

        # supported institutions
        institutions_types = TYPE_CHOICES
        institutions = Institution.objects.all()

        ctx = {
            "institutions": institutions,
            "institutions_count": institutions_count,
            "institutions_types": institutions_types,
            "donations_count": donations_count,
        }
        return render(request, 'index.html', ctx)


class AddDonation(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        categories = Category.objects.all()

        ctx = {
            "categories": categories,
        }
        return render(request, 'form.html', ctx)

    def post(self, request):
        if request.user.is_authenticated:
            selected_categories = request.POST.getlist('categories', [])
            bags_amount = request.POST.get('bags', None)
            selected_organization = Institution.objects.get(pk=request.POST.get('organization', None))
            street_name = request.POST.get('address', None)
            city_name = request.POST.get('city', None)
            postcode = request.POST.get('postcode', None)
            phone_num = request.POST.get('phone', None)
            date = request.POST.get('data', None)
            time = request.POST.get('time', None)
            pick_up_comment = request.POST.get('more_info', None)
            user = request.user
            new_donation = Donation.objects.create(quantity=bags_amount,
                                                   institution=selected_organization,
                                                   address=street_name,
                                                   phone_number=phone_num,
                                                   city=city_name,
                                                   zip_code=postcode,
                                                   pick_up_date=date,
                                                   pick_up_time=time,
                                                   pick_up_comment=pick_up_comment,
                                                   user=user)
            for pk in selected_categories:
                new_donation.categories.add(int(pk))
            return redirect('donation_success')
        else:
            return HttpResponse('error - check form input')


def get_institutions(request):
    # filtering institutions by selected category
    selected_categories = request.GET.getlist('categories', [])
    institutions = Institution.objects.filter(categories__in=selected_categories).distinct()

    ctx = {
        "institutions": institutions,
    }
    return render(request, 'form_institutions.html', ctx)


class DonationSuccessView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None and user.is_authenticated:
                login(request, user)
                if 'next' in self.request.GET:
                    return redirect(self.request.GET.get('next'))
                else:
                    return redirect('index')
            else:
                return redirect('register')
        else:
            return HttpResponse('Error')


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('index')


class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            return redirect('login')
        else:
            form = RegisterForm()
        return render(request, 'register.html', {"form": form})


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            user_data = UserProfile.objects.get(user=request.user)
            user_donations = Donation.objects.filter(user=request.user).order_by('is_taken', '-pick_up_date')
            ctx = {
                "user_data": user_data,
                "user_donations": user_donations,
            }
            return render(request, "profile.html", ctx)
        else:
            return redirect('login')

    def post(self, request):
        if "donation_id" in request.POST and request.user.is_authenticated:
            donation_id = request.POST.get("donation_id", None)
            selected_donation = Donation.objects.get(pk=donation_id)
            if selected_donation.is_taken is False:
                selected_donation.is_taken = True
                selected_donation.save()
            else:
                pass
        return redirect('profile')


class UserProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            form = UserUpdateForm(instance=request.user)
            ctx = {
                "form": form,
            }
            return render(request, "profile_update_form.html", ctx)
        else:
            return redirect('login')

    def post(self, request):
        data_update = UserUpdateForm(request.POST, instance=request.user)
        success = request.user.check_password(request.POST['password'])
        if data_update.is_valid() and success:
            data_update.save()
            return redirect('profile')
        else:
            return redirect('profile_update')


class PasswordChangeView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            form = PasswordChangeForm(request.user)
            ctx = {
                "form": form
            }
            return render(request, "change_password.html", ctx)
        else:
            redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'You have changed your password.')
                return redirect('profile_update')
            else:
                messages.error(request, 'An error occurred!')
