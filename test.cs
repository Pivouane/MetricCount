class entity
{
    string tag;
    int health; 
    float speed;
    int damage;
    bool is_dead = false;

    Random rnd = new Random();
    double luck;
    string get_tag()
    {return tag;}

    int get_health()
    {return health;}

    float get_speed()
    {return speed;}

    int get_damage()
    {return damage;}

    void entity_set(string _tag, int _health, float _speed , int _damage)
    {
        tag = _tag;
        health = _health; 
        speed = _speed;
        damage = _damage;
    }
    void take_damage(int _damage)
    {
        health -= _damage;
        if(health <= 0)
        {is_dead = true;}
    }
}



class axel 
{
    entity ent = new entity();
    ent.entity_set("axel", 10, 2, 4 );
    float crit_chance = 0.15f;
    float armor = 1.12f;
    void printhealth()
    {
        console.writeline(str(ent.get_health)); 
    }
}

class ploplo
{
    entity ent = new entity(); 
    ent.entity("ploplo" , 6, 3 , 5); 
    float armor = 0.9;
    float beauty = 0.6;
    void printhealth()
    {
        console.writeline(str(ent.get_health)); 
    }
}

class lebeheun
{
    entity ent = new entity();
    ent.entity_set("lebeheun", 8, 4, 0);
    int money = 100;
    float armor = 1;  
    void set_money(int money_wl)
    {money += money_wl;}
    int get_money()
    {return money;}
    void printhealth()
    {
        console.writeline(str(ent.get_health)); 
    }
    
}

class weapon 
{
    int dam;
    float acc;
    void set(int damage , accuracy)
    {
        dam = damage;
        acc = accuracy; 
    }
    inventory inv = new inventory();    
    inv.upgrade();
}

class inventory 
{
    List<weapon> items = new List<weapon>; 
    weapon sword = new weapon(); 
    sword.set(4,8);
    void upgrade()
    {
        sword.damage += 1;
    }
}