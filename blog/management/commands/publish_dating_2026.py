from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from blog.models import BlogPost, BlogCategory


class Command(BaseCommand):
    help = 'Publish the Dating in 2026 article'

    def handle(self, *args, **options):
        # Get or create author
        author, created = User.objects.get_or_create(
            username='egy360_editor',
            defaults={
                'email': 'editor@360egy.com',
                'first_name': 'Egy360',
                'last_name': 'Editorial',
                'is_staff': True,
            }
        )
        if created:
            author.set_password('changeme123')
            author.save()
            self.stdout.write(f"Created author: {author.username}")

        # Get or create category
        category, created = BlogCategory.objects.get_or_create(
            name='Life & Relationships',
            defaults={'slug': 'life-relationships'}
        )
        if created:
            self.stdout.write(f"Created category: {category.name}")

        # Article content
        article_content = """Let me ask you something. Do you know a guy who works hard, earns a decent salary, but somehow cannot afford to take a girl out twice in the same month?

Now do you know a girl who works the same job, maybe even earns less, but somehow never pays for anything? Free dinners, free entry to concerts, free rides, free attention.

Same job. Same city. Same age. Completely different world.

That is the reality of dating in 2026, and nobody is talking about it honestly.

Here is what no one wants to admit.

A pretty girl walking into a restaurant has someone offering to pay before she even sits down. A decent-looking guy doing the same job, sometimes working harder because he knows he has no backup, is counting coins at the end of the month. He eats alone, watches Netflix alone, and wonders why he even tries.

He is not lazy. He is not unattractive. He is simply broke in a world where his appearance cannot buy him free dinners or open doors that closed long ago.

Now here is where it gets complicated.

When it is time for marriage, the same society that encouraged equality and independence suddenly shifts. The family expects the man to have an apartment, a car, savings for the wedding, and the ability to provide. No one asks the woman to contribute equally to these costs.

But she was just told she is equal. So which is it?

This creates a gap that neither side understands. Women are confused about what they should expect. Men are confused about what they are supposed to provide. And the ones caught in the middle are the ones genuinely looking for love.

Here is another observation that will make you laugh, then cry.

A girl in most social circles has what we call "options." She has three or four guys in her chat who text her regularly, buy her coffee when she is bored, and compete for her attention. She enjoys this. It feels good to be wanted. So she keeps them there, never fully committing to any, because commitment would mean losing the others.

None of these men know they are in a rotation. Each one thinks he has a chance.

Meanwhile, a genuinely interested guy in the same circle is just one of four. He is not flashy enough to stand out. He gets ignored while competing for attention that was never meant for him.

This is not about all women. Most women are not like this. But enough are, and it is destroying the dating market for everyone.

Now let us talk about the elephant in the room. Egypt's divorce rate reached nearly 70 percent. Let that number sink in.

Why? Because people are getting married without understanding what they are actually signing up for. The dating process has become so broken that by the time someone gets married, they are already desperate, not actually compatible.

And the ones who see this clearly? They are opting out.

I know men in their early thirties who have completely withdrawn. They stopped approaching women. They stopped using dating apps. They focused on their careers, their health, their peace. They learned to enjoy their own company, their own income, their own freedom.

And honestly? They seem happier.

When you get nothing but rejection, when every attempt costs you money you do not have, when you watch women you genuinely like choose guys who treat them poorly, at some point self-preservation kicks in.

They are not bitter. They are just tired.

So here we are in 2026, with more connection technology than ever, but somehow more loneliness. With more options than ever, but less real connection. With equal rights rhetoric, but unequal expectations.

I do not have all the answers. Maybe there are no answers. Maybe the system is just broken, and the only logical response is to focus on yourself, build your peace, and hope something changes.

Or maybe, just maybe, we need to start being honest about what is actually happening.

Not to blame anyone. Not to point fingers. But to understand the model so we can navigate it better.

The question is: Are you still playing the game, or have you quietly left the table?"""

        excerpt = "An honest look at the modern dating crisis. Why are good men and women struggling to find meaningful connections in Egypt and abroad? The problems, root causes, and what we can do about it."

        meta_description = "Dating in 2026: An honest analysis of why good people cannot find each other. Statistics, the attention economy asymmetry, and the emerging withdrawal of men from dating."

        tags = "dating 2026, modern dating, relationship advice, dating crisis, egypt dating, finding love, divorce rate egypt"

        # Create the post
        slug = slugify("dating-in-2026-a-quiet-goodbye")

        post, created = BlogPost.objects.get_or_create(
            slug=slug,
            defaults={
                'title': 'Dating in 2026: A Quiet Goodbye',
                'author': author,
                'category': category,
                'content': article_content,
                'excerpt': excerpt,
                'meta_description': meta_description,
                'tags': tags,
                'status': 'published',
                'published_at': timezone.now(),
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created post: {post.title}"))
            self.stdout.write(self.style.SUCCESS(f"Post URL: /blog/{slug}/"))
        else:
            self.stdout.write(self.style.WARNING(f"Post already exists: {post.title}"))

        self.stdout.write(self.style.SUCCESS("\nArticle published successfully!"))
        self.stdout.write(f"URL: https://360egy.com/blog/{slug}/")